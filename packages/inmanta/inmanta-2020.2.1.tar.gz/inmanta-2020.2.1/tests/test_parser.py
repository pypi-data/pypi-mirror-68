"""
    Copyright 2016 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import re
import warnings
from typing import List

import pytest

from inmanta.ast import LocatableString, Namespace
from inmanta.ast.blocks import BasicBlock
from inmanta.ast.constraint.expression import And, Equals, GreaterThan, In, IsDefined, Not, Or, Regex
from inmanta.ast.statements import ExpressionStatement, Literal, ReferenceStatement, define
from inmanta.ast.statements.assign import (
    Assign,
    CreateDict,
    CreateList,
    IndexLookup,
    MapLookup,
    SetAttribute,
    ShortIndexLookup,
    StringFormat,
)
from inmanta.ast.statements.call import FunctionCall
from inmanta.ast.statements.define import (
    DefineEntity,
    DefineImplement,
    DefineIndex,
    DefineTypeConstraint,
    DefineTypeDefault,
    TypeDeclaration,
)
from inmanta.ast.statements.generator import Constructor, If
from inmanta.ast.variables import AttributeReference, Reference
from inmanta.execute.util import NoneValue
from inmanta.parser import ParserException, SyntaxDeprecationWarning
from inmanta.parser.plyInmantaParser import parse


def parse_code(model_code: str):
    root_ns = Namespace("__root__")
    main_ns = Namespace("__config__")
    main_ns.parent = root_ns
    statements = parse(main_ns, "test", model_code)

    return statements


def test_define_empty():
    parse_code("""""")


def test_define_entity():
    """Test the definition of entities
    """
    statements = parse_code(
        """
entity Test:
end
entity Other:
string hello
end
entity Other:
 \"\"\"XX
 \"\"\"
end
"""
    )

    assert len(statements) == 3

    stmt = statements[0]
    assert isinstance(stmt, define.DefineEntity)
    assert stmt.name == "Test"
    assert [str(p) for p in stmt.parents] == ["std::Entity"]
    assert len(stmt.attributes) == 0
    assert stmt.comment is None
    assert stmt.type.comment is None


def test_undefine_default():
    statements = parse_code(
        """
entity Test extends Foo:
 string hello = undef
 string[] dinges = undef
end"""
    )
    assert len(statements) == 1

    stmt = statements[0]
    assert isinstance(stmt, define.DefineEntity)
    assert stmt.name == "Test"
    assert [str(p) for p in stmt.parents] == ["Foo"]
    assert len(stmt.attributes) == 2
    assert stmt.comment is None
    assert stmt.type.comment is None

    for ad in stmt.attributes:
        assert isinstance(ad.type, TypeDeclaration)
        assert isinstance(ad.type.basetype, LocatableString)
        assert isinstance(ad.name, LocatableString)
        assert ad.default is None
        assert ad.remove_default

    assert str(stmt.attributes[0].name) == "hello"
    assert str(stmt.attributes[1].name) == "dinges"


def test_extend_entity():
    """Test extending entities
    """
    statements = parse_code(
        """
entity Test extends Foo:
end
"""
    )

    assert len(statements) == 1

    stmt = statements[0]
    assert [str(p) for p in stmt.parents] == ["Foo"]


def test_complex_entity():
    """Test definition of a complex entity
    """
    documentation = "This entity has documentation"
    statements = parse_code(
        """
entity Test extends Foo, foo::sub::Bar:
    \"\"\" %s
    \"\"\"
    string hello
    bool bar = true
    number? ten=5
end
"""
        % documentation
    )

    assert len(statements) == 1

    stmt = statements[0]
    assert len(stmt.parents) == 2
    assert [str(p) for p in stmt.parents] == ["Foo", "foo::sub::Bar"]
    assert str(stmt.comment).strip() == documentation
    assert str(stmt.type.comment).strip() == documentation
    assert len(stmt.attributes) == 3

    for ad in stmt.attributes:
        assert isinstance(ad.type, TypeDeclaration)
        assert isinstance(ad.type.basetype, LocatableString)
        assert isinstance(ad.name, LocatableString)

    assert str(stmt.attributes[0].name) == "hello"
    assert str(stmt.attributes[1].name) == "bar"
    assert str(stmt.attributes[2].name) == "ten"

    assert stmt.attributes[1].default.execute(None, None, None)

    assert stmt.attributes[2].default.execute(None, None, None) == 5


def test_relation():
    """Test definition of relations
    """
    statements = parse_code(
        """
Test tests [0:] -- [5:10] Foo bars
"""
    )

    assert len(statements) == 1
    rel = statements[0]

    assert len(rel.left) == 3
    assert len(rel.right) == 3

    assert str(rel.left[0]) == "Test"
    assert str(rel.right[0]) == "Foo"

    assert str(rel.left[1]) == "tests"
    assert str(rel.right[1]) == "bars"

    assert rel.left[2] == (0, None)
    assert rel.right[2] == (5, 10)


def test_relation_2():
    """Test definition of relations
    """
    statements = parse_code(
        """
Test tests [3] -- [:10] Foo bars
"""
    )

    assert len(statements) == 1
    rel = statements[0]

    assert len(rel.left) == 3
    assert len(rel.right) == 3

    assert str(rel.left[0]) == "Test"
    assert str(rel.right[0]) == "Foo"

    assert str(rel.left[1]) == "tests"
    assert str(rel.right[1]) == "bars"

    assert rel.left[2] == (3, 3)
    assert rel.right[2] == (None, 10)


def test_new_relation():
    """Test definition of relations
    """
    statements = parse_code(
        """
Test.bar [1] -- Foo.tests [5:10]
"""
    )

    assert len(statements) == 1, "Should return four statements"
    rel = statements[0]

    assert len(rel.left) == 3
    assert len(rel.right) == 3

    assert str(rel.left[0]) == "Test"
    assert str(rel.right[0]) == "Foo"

    assert str(rel.left[1]) == "tests"
    assert str(rel.right[1]) == "bar"

    assert rel.left[2] == (5, 10)
    assert rel.right[2] == (1, 1)


def test_new_relation_with_annotations():
    """Test definition of relations
    """
    statements = parse_code(
        """
Test.bar [1] foo,bar Foo.tests [5:10]
"""
    )

    assert len(statements) == 1, "Should return four statements"
    rel = statements[0]

    assert len(rel.left) == 3
    assert len(rel.right) == 3

    assert str(rel.left[0]) == "Test"
    assert str(rel.right[0]) == "Foo"

    assert str(rel.left[1]) == "tests"
    assert str(rel.right[1]) == "bar"

    assert rel.left[2] == (5, 10)
    assert rel.right[2] == (1, 1)
    assert len(rel.annotations) == 2
    assert rel.annotation_expression[0][1].name == "foo"
    assert rel.annotation_expression[1][1].name == "bar"


def test_new_relation_unidir():
    """Test definition of relations
    """
    statements = parse_code(
        """
Test.bar [1] -- Foo
"""
    )

    assert len(statements) == 1, "Should return four statements"
    rel = statements[0]

    assert len(rel.left) == 3
    assert len(rel.right) == 3

    assert str(rel.left[0]) == "Test"
    assert str(rel.right[0]) == "Foo"

    assert (rel.left[1]) is None
    assert str(rel.right[1]) == "bar"

    assert rel.left[2] is None
    assert rel.right[2] == (1, 1)


def test_new_relation_with_annotations_unidir():
    """Test definition of relations
    """
    statements = parse_code(
        """
Test.bar [1] foo,bar Foo
"""
    )

    assert len(statements) == 1, "Should return four statements"
    rel = statements[0]

    assert len(rel.left) == 3
    assert len(rel.right) == 3

    assert str(rel.left[0]) == "Test"
    assert str(rel.right[0]) == "Foo"

    assert rel.left[1] is None
    assert str(rel.right[1]) == "bar"

    assert rel.left[2] is None
    assert rel.right[2] == (1, 1)
    assert len(rel.annotations) == 2
    assert rel.annotation_expression[0][1].name == "foo"
    assert rel.annotation_expression[1][1].name == "bar"


def test_implementation():
    """Test the definition of implementations
    """
    statements = parse_code(
        """
implementation test for Test:
end
"""
    )

    assert len(statements) == 1
    assert len(statements[0].block.get_stmts()) == 0
    assert statements[0].name == "test"
    assert isinstance(statements[0].entity, LocatableString)

    statements = parse_code(
        """
implementation test for Test:
    std::File(attr="a")
    var = hello::func("world")
end
"""
    )

    assert len(statements) == 1
    assert len(statements[0].block.get_stmts()) == 2


def test_implementation_with_for():
    """Test the propagation of type requires when using a for
    """
    statements = parse_code(
        """
implementation test for Test:
    \"\"\" test \"\"\"
    for v in data:
        std::template("template")
    end
end
"""
    )

    assert len(statements) == 1
    assert len(statements[0].block.get_stmts()) == 1


def test_implements():
    """Test implements with no selector
    """
    statements = parse_code(
        """
implement Test using test
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert str(stmt.entity) == "Test"
    assert [str(i) for i in stmt.implementations] == ["test"]
    assert str(stmt.select) == "true"


def test_implements_2():
    """Test implements with selector
    """
    statements = parse_code(
        """
implement Test using test, blah when (self > 5)
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert str(stmt.entity) == "Test"
    assert [str(p) for p in stmt.implementations] == ["test", "blah"]
    assert isinstance(stmt.select, GreaterThan)
    assert stmt.select.children[0].name == "self"
    assert stmt.select.children[1].value == 5


def test_implements_parent():
    statements = parse_code(
        """
implement Test using parents  \""" testc \"""
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert str(stmt.entity) == "Test"
    assert stmt.inherit is True


@pytest.mark.parametrize(
    "implementations",
    [["parents", "std::none"], ["std::none", "parents"], ["i1", "parents", "i2"], ["std::none"], ["i1", "i2"]],
)
def test_implements_parent_in_list(implementations: List[str]):
    statements = parse_code(
        """
implement Test using %s
        """
        % ", ".join(implementations)
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert str(stmt.entity) == "Test"
    assert stmt.inherit is ("parents" in implementations)
    assert [str(i) for i in stmt.implementations] == [i for i in implementations if i != "parents"]


def test_implements_selector():
    """Test implements with selector
    """
    statements = parse_code(
        """
implement Test using test when not (fg(self) and false)
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert str(stmt.entity) == "Test"
    assert [str(i) for i in stmt.implementations] == ["test"]
    assert isinstance(stmt.select, Not)
    assert isinstance(stmt.select.children[0], And)
    assert isinstance(stmt.select.children[0].children[0], FunctionCall)
    assert isinstance(stmt.select.children[0].children[1], Literal)


def test_regex():
    statements = parse_code(
        """
a = /[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}/
"""
    )

    assert len(statements) == 1
    stmt = statements[0].value
    assert isinstance(stmt, Regex)
    assert stmt.children[1].value == re.compile(r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}")


def test_regex_backslash():
    statements = parse_code(
        r"""
a = /\\/
"""
    )

    assert len(statements) == 1
    stmt = statements[0].value
    assert isinstance(stmt, Regex)
    assert stmt.children[1].value == re.compile(r"\\")


def test_regex_escape():
    statements = parse_code(
        r"""
a = /\/1/
"""
    )

    assert len(statements) == 1
    stmt = statements[0].value
    assert isinstance(stmt, Regex)
    assert stmt.children[1].value == re.compile(r"\/1")


def test_regex_twice():
    statements = parse_code(
        r"""
a = /\/1/
b = "v"
c = /\/1/
"""
    )

    assert len(statements) == 3
    stmt = statements[0].value
    assert isinstance(stmt, Regex)
    assert stmt.children[1].value == re.compile(r"\/1")


def test_1584_regex_error():
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
a = /)/
            """
        )

    exception: ParserException = pytest_e.value
    assert exception.location.file == "test"
    assert exception.location.lnr == 2
    assert exception.location.start_char == 5
    assert exception.location.end_lnr == 2
    assert exception.location.end_char == 8
    assert exception.value == "/)/"
    assert exception.msg == "Syntax error: Regex error in /)/: 'unbalanced parenthesis at position 0'"


def test_typedef():
    statements = parse_code(
        """
typedef uuid as string matching /[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}/
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineTypeConstraint)
    assert str(stmt.name) == "uuid"
    assert str(stmt.basetype) == "string"
    assert isinstance(stmt.get_expression(), Regex)
    assert stmt.get_expression().children[1].value == re.compile(
        r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
    )


def test_typedef_in():
    statements = parse_code(
        """
typedef abc as string matching self in ["a","b","c"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineTypeConstraint)
    assert str(stmt.name) == "abc"
    assert str(stmt.basetype) == "string"
    assert isinstance(stmt.get_expression(), In)
    assert [x.value for x in stmt.get_expression().children[1].items] == ["a", "b", "c"]


def test_typedef_plugin_call():
    """
    If this test fails, the collection of validation types and
    validation_parameters will fail in the LSM module.
    plugin_call() must expand to (plugin_call() == true)
    """
    statements = parse_code(
        """
typedef abc as string matching std::is_base64_encoded(self)
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineTypeConstraint)
    assert str(stmt.name) == "abc"
    assert str(stmt.basetype) == "string"
    assert isinstance(stmt.get_expression(), Equals)
    left_side_equals = stmt.get_expression()._arguments[0]
    right_side_equals = stmt.get_expression()._arguments[1]
    assert isinstance(left_side_equals, FunctionCall)
    assert isinstance(right_side_equals, Literal)
    assert isinstance(right_side_equals.value, bool) and right_side_equals.value


def test_typedef2():
    statements = parse_code(
        """
typedef ConfigFile as File(mode = 644, owner = "root", group = "root")
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineTypeDefault)
    assert stmt.name == "ConfigFile"
    assert isinstance(stmt.ctor, Constructor)


def test_index():
    statements = parse_code(
        """
index File(host, path)
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineIndex)
    assert str(stmt.type) == "File"
    assert stmt.attributes == ["host", "path"]


def test_ctr():
    statements = parse_code(
        """
File(host = 5, path = "Jos")
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Constructor)
    assert str(stmt.class_type) == "File"
    assert {k: v.value for k, v in stmt.attributes.items()} == {"host": 5, "path": "Jos"}


def test_ctr_dict():
    statements = parse_code(
        """
dct = { "host": "myhost", "path": "/dir/file" }
File(**dct)
"""
    )

    assert len(statements) == 2
    stmt = statements[1]
    assert isinstance(stmt, Constructor)
    assert str(stmt.class_type) == "File"
    assert stmt.attributes == {}
    assert len(stmt.wrapped_kwargs) == 1


def test_ctr_dict_multi_param():
    statements = parse_code(
        """
dct = { "host": "myhost" }
File(**dct, path = "/dir/file")
"""
    )

    assert len(statements) == 2
    stmt = statements[1]
    assert isinstance(stmt, Constructor)
    assert str(stmt.class_type) == "File"
    assert {k: v.value for k, v in stmt.attributes.items()} == {"path": "/dir/file"}
    assert len(stmt.wrapped_kwargs) == 1


def test_ctr_dict_multi_param3():
    statements = parse_code(
        """
dct = { "host": "myhost" }
File(path = "/dir/file", **dct)
"""
    )

    assert len(statements) == 2
    stmt = statements[1]
    assert isinstance(stmt, Constructor)
    assert str(stmt.class_type) == "File"
    assert {k: v.value for k, v in stmt.attributes.items()} == {"path": "/dir/file"}
    assert len(stmt.wrapped_kwargs) == 1


def test_indexlookup():
    statements = parse_code(
        """
a=File[host = 5, path = "Jos"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0].value
    assert isinstance(stmt, IndexLookup)
    assert str(stmt.index_type) == "File"
    assert {k: v.value for k, v in stmt.query} == {"host": 5, "path": "Jos"}


def test_indexlookup_kwargs():
    statements = parse_code(
        """
dct = {"path": "/dir/file"}
a=File[host = "myhost", **dct]
"""
    )

    assert len(statements) == 2
    stmt = statements[1].value
    assert isinstance(stmt, IndexLookup)
    assert str(stmt.index_type) == "File"
    assert {k: v.value for k, v in stmt.query} == {"host": "myhost"}
    assert len(stmt.wrapped_query) == 1


def test_short_index_lookup():
    statements = parse_code(
        """
a = vm.files[path="/etc/motd"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0].value
    assert isinstance(stmt, ShortIndexLookup)
    assert isinstance(stmt.rootobject, Reference)
    assert stmt.rootobject.name == "vm"
    assert stmt.relation == "files"
    assert {k: v.value for k, v in stmt.querypart} == {"path": "/etc/motd"}


def test_short_index_lookup_kwargs():
    statements = parse_code(
        """
dct = {"path": "/etc/motd"}
a = vm.files[**dct]
"""
    )

    assert len(statements) == 2
    stmt = statements[1].value
    assert isinstance(stmt, ShortIndexLookup)
    assert isinstance(stmt.rootobject, Reference)
    assert stmt.rootobject.name == "vm"
    assert stmt.relation == "files"
    assert stmt.querypart == []
    assert len(stmt.wrapped_querypart) == 1


def test_ctr_2():
    statements = parse_code(
        """
File( )
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Constructor)
    assert str(stmt.class_type) == "File"
    assert {k: v.value for k, v in stmt.attributes.items()} == {}


def test_function():
    statements = parse_code(
        """
file( )
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, FunctionCall)
    assert str(stmt.name) == "file"


def test_function_2():
    statements = parse_code(
        """
file(b)
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, FunctionCall)
    assert str(stmt.name) == "file"


def test_function_3():
    statements = parse_code(
        """
file(b,)
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, FunctionCall)
    assert str(stmt.name) == "file"


def test_list_def():
    statements = parse_code(
        """
a=["a]","b"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, CreateList)
    assert [x.value for x in stmt.value.items] == ["a]", "b"]


def test_list_def_trailing_comma():
    statements = parse_code(
        """
a=["a]","b",]
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, CreateList)
    assert [x.value for x in stmt.value.items] == ["a]", "b"]


def test_map_def():
    statements = parse_code(
        """
a={ "a":"b", "b":1}
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, CreateDict)
    assert [(x[0], x[1].value) for x in stmt.value.items] == [("a", "b"), ("b", 1)]


def test_map_def_var():
    statements = parse_code("""a={ "b":b}""")
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, CreateDict)
    assert isinstance(stmt.value.items[0][1], Reference)


def test_map_def_list():
    statements = parse_code("""a={ "a":["a"]}""")
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, CreateDict)
    assert isinstance(stmt.value.items[0][1], CreateList)


def test_map_def_map():
    statements = parse_code("""a={ "a":{"a":"C"}}""")
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, CreateDict)
    assert isinstance(stmt.value.items[0][1], CreateDict)


def test_booleans():
    statements = parse_code(
        """
a=true b=false
"""
    )

    assert len(statements) == 2
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert stmt.value.value
    assert not statements[1].value.value


def test_none():
    statements = parse_code(
        """
a=null
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value.value, NoneValue)


def test_numbers():
    statements = parse_code(
        """
a=1
b=2.0
c=-5
d=-0.256
"""
    )

    assert len(statements) == 4
    values = [1, 2.0, -5, -0.256]
    for i in range(4):
        stmt = statements[i]
        assert isinstance(stmt, Assign)
        assert stmt.value.value == values[i]


def test_string():
    statements = parse_code(
        """
a="jos"
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == "jos"


def test_string_2():
    statements = parse_code(
        """
a='jos'
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == "jos"


def test_string_backslash():
    statements = parse_code(
        """
a="\\\\"
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == "\\"


def test_string_backslash_2():
    statements = parse_code(
        """
a='\\\\'
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == "\\"


def test_empty():
    statements = parse_code(
        """
a=""
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == ""


def test_empty_2():
    statements = parse_code(
        """
a=''
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == ""


def test_string_format():
    statements = parse_code(
        """
a="j{{o}}s"
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, StringFormat)
    assert isinstance(stmt.value._variables[0][0], Reference)
    assert [x[0].name for x in stmt.value._variables] == ["o"]


def test_string_format_2():
    statements = parse_code(
        """
a="j{{c.d}}s"
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, StringFormat)
    assert len(stmt.value._variables) == 1
    assert len(stmt.value._variables[0]) == 2
    assert isinstance(stmt.value._variables[0][0], AttributeReference)
    assert stmt.value._variables[0][0].instance.name == "c"
    assert stmt.value._variables[0][0].attribute == "d"


def test_attribute_reference():
    statements = parse_code(
        """
a=a::b::c.d
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, AttributeReference)
    assert isinstance(stmt.value.instance, Reference)
    assert stmt.value.instance.full_name == "a::b::c"
    assert stmt.value.attribute == "d"


def test_is_defined():
    statements = parse_code(
        """
implement Test1 using tt when self.other is defined
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert isinstance(stmt.select, IsDefined)
    assert stmt.select.attr.name == "self"
    assert stmt.select.name == "other"


def test_is_defined_implicit_self():
    statements = parse_code(
        """
implement Test1 using tt when other is defined
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert isinstance(stmt.select, IsDefined)
    assert stmt.select.attr is None
    assert stmt.select.name == "other"


def test_is_defined_short():
    statements = parse_code(
        """
implement Test1 using tt when a.other is defined
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert isinstance(stmt.select, IsDefined)
    assert isinstance(stmt.select.attr, Reference)
    assert stmt.select.attr.name == "a"
    assert stmt.select.name == "other"


def assert_is_non_value(x):
    assert isinstance(x, Literal)
    assert isinstance(x.value, NoneValue)


def compare_attr(attr, name, mytype, defs, multi=False, opt=False):
    assert str(attr.name) == name
    defs(attr.default)
    assert attr.type.multi == multi
    assert str(attr.type.basetype) == mytype
    assert attr.type.nullable == opt


def assert_is_none(x):
    assert x is None


def assert_equals(x, y):
    assert x == y


def test_define_list_attribute():
    statements = parse_code(
        """
entity Jos:
  bool[] bar
  ip::ip[] ips = ["a"]
  string[] floom = []
  string[] floomx = ["a", "b"]
  string[]? floomopt = null
end"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineEntity)
    assert len(stmt.attributes) == 5

    compare_attr(stmt.attributes[0], "bar", "bool", assert_is_none, multi=True)
    compare_attr(stmt.attributes[2], "floom", "string", lambda x: assert_equals([], x.items), multi=True)

    def compare_default(list):
        def comp(x):
            assert len(list) == len(x.items)
            for one, it in zip(list, x.items):
                assert isinstance(it, Literal)
                assert it.value == one

        return comp

    compare_attr(stmt.attributes[1], "ips", "ip::ip", compare_default(["a"]), multi=True)
    compare_attr(stmt.attributes[3], "floomx", "string", compare_default(["a", "b"]), multi=True)
    compare_attr(stmt.attributes[4], "floomopt", "string", assert_is_non_value, opt=True, multi=True)


def test_define_dict_attribute():
    statements = parse_code(
        """
entity Jos:
  dict bar
  dict foo = {}
  dict blah = {"a":"a"}
  dict? xxx = {"a":"a"}
  dict? xxxx = null
end"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineEntity)
    assert len(stmt.attributes) == 5

    compare_attr(stmt.attributes[0], "bar", "dict", assert_is_none)
    compare_attr(stmt.attributes[1], "foo", "dict", lambda x: assert_equals([], x.items))

    def compare_default(list):
        def comp(x):
            assert len(list) == len(x.items)
            for (ok, ov), (k, v) in zip(list, x.items):
                assert k == ok
                assert ov == v.value

        return comp

    compare_attr(stmt.attributes[2], "blah", "dict", compare_default([("a", "a")]))
    compare_attr(stmt.attributes[3], "xxx", "dict", compare_default([("a", "a")]), opt=True)
    compare_attr(stmt.attributes[4], "xxxx", "dict", assert_is_non_value, opt=True)


def test_lexer():
    parse_code(
        """
#test
//test2
a=0.5
b=""
"""
    )


def test_eol_comment():
    parse_code(
        """a="a"
    # valid_target_types: tosca.capabilities.network.Bindable"""
    )


def test_mls():
    statements = parse_code(
        """
entity MANO:
    \"""
        This entity provides management, orchestration and monitoring

        More test
    \"""
end
"""
    )
    assert len(statements) == 1
    stmt = statements[0]

    assert isinstance(stmt, DefineEntity)

    mls = stmt.comment

    print(mls)

    assert (
        str(mls)
        == """
        This entity provides management, orchestration and monitoring

        More test
    """
    )

    assert (
        str(stmt.type.comment)
        == """
        This entity provides management, orchestration and monitoring

        More test
    """
    )


def test_bad():
    with pytest.raises(ParserException):
        parse_code(
            """
a = b.c
a=a::b::c.
"""
        )


def test_bad_2():
    with pytest.raises(ParserException):
        parse_code(
            """
a=|
"""
        )


def test_error_on_relation():
    with pytest.raises(ParserException) as e:
        parse_code(
            """
Host.provider [1] -- Provider test"""
        )
    assert e.value.location.file == "test"
    assert e.value.location.lnr == 3
    assert e.value.location.start_char == 2


def test_doc_string_on_new_relation():
    statements = parse_code(
        """
File.host [1] -- Host
\"""
Each file needs to be associated with a host
\"""
"""
    )
    assert len(statements) == 1

    stmt = statements[0]
    assert str(stmt.comment).strip() == "Each file needs to be associated with a host"


def test_doc_string_on_relation():
    statements = parse_code(
        """
File file [1] -- [0:] Host host
\"""
Each file needs to be associated with a host
\"""
"""
    )
    assert len(statements) == 1

    stmt = statements[0]
    assert str(stmt.comment).strip() == "Each file needs to be associated with a host"


def test_doc_string_on_typedef():
    statements = parse_code(
        """
typedef foo as string matching /^a+$/
\"""
    Foo is a stringtype that only allows "a"
\"""
"""
    )
    assert len(statements) == 1

    stmt = statements[0]
    assert str(stmt.comment).strip() == 'Foo is a stringtype that only allows "a"'


def test_doc_string_on_typedefault():
    statements = parse_code(
        """
typedef Foo as File(x=5)
\"""
    Foo is a stringtype that only allows "a"
\"""
"""
    )
    assert len(statements) == 1

    stmt = statements[0]
    assert str(stmt.comment).strip() == 'Foo is a stringtype that only allows "a"'


def test_doc_string_on_impl():
    statements = parse_code(
        """
implementation test for Host:
    \"""
        Bla bla
    \"""
end
"""
    )
    assert len(statements) == 1

    stmt = statements[0]
    assert str(stmt.comment).strip() == "Bla bla"
    assert str(stmt.type.comment).strip() == "Bla bla"


def test_doc_string_on_implements():
    statements = parse_code(
        """
implement Host using test
\"""
    Always use test!
\"""
\"""
    Not a comment
\"""

"""
    )
    assert len(statements) == 2

    stmt = statements[0]
    assert str(stmt.comment).strip() == "Always use test!"


def test_precise_lexer_positions():
    statements = parse_code(
        """
implement Test1 using tt when self.other is defined
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, DefineImplement)
    assert isinstance(stmt.select, IsDefined)
    assert stmt.select.attr.name == "self"
    assert str(stmt.select.name) == "other"


def test_list_extend_bad():
    with pytest.raises(ParserException):
        parse_code(
            """
    a+=b
    """
        )


def test_list_extend_good():
    statements = parse_code(
        """
z.a+=b
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, SetAttribute)
    assert stmt.list_only is True
    assert isinstance(stmt.value, Reference)
    assert stmt.value.name == "b"


def test_mapref():
    """Test extending entities
    """
    statements = parse_code(
        """
a = b.c["test"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, MapLookup)
    assert isinstance(stmt.value.themap, AttributeReference)
    assert stmt.value.themap.instance.name == "b"
    assert stmt.value.themap.attribute == "c"
    assert isinstance(stmt.value.key, Literal)
    assert stmt.value.key.value == "test"


def test_mapref_2():
    """Test extending entities
    """
    statements = parse_code(
        """
a = c["test"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, MapLookup)
    assert isinstance(stmt.value.themap, Reference)
    assert stmt.value.themap.name == "c"
    assert isinstance(stmt.value.key, Literal)
    assert stmt.value.key.value == "test"


def test_map_multi_ref():
    """Test extending entities
    """
    statements = parse_code(
        """
a = c["test"]["xx"]
"""
    )

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, Assign)
    assert isinstance(stmt.value, MapLookup)
    assert isinstance(stmt.value.themap, MapLookup)
    assert isinstance(stmt.value.themap.themap, Reference)
    assert stmt.value.themap.themap.name == "c"
    assert isinstance(stmt.value.key, Literal)
    assert stmt.value.key.value == "xx"
    assert isinstance(stmt.value.themap.key, Literal)
    assert stmt.value.themap.key.value == "test"


def test_if_statement():
    """Test for the if statement
    """
    statements = parse_code(
        """
if test.field == "value":
    test.other = "otherValue"
end
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, If)
    assert isinstance(stmt.condition, ExpressionStatement)
    assert isinstance(stmt.if_branch, BasicBlock)
    assert len(stmt.if_branch.get_stmts()) == 1
    assert isinstance(stmt.else_branch, BasicBlock)
    assert len(stmt.else_branch.get_stmts()) == 0


def test_if_else():
    """Test for the if statement with an else clause
    """
    statements = parse_code(
        """
if test.field == "value":
    test.other = "otherValue"
else:
    test.other = "altValue"
end
"""
    )
    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, If)
    assert isinstance(stmt.condition, ExpressionStatement)
    assert isinstance(stmt.if_branch, BasicBlock)
    assert len(stmt.if_branch.get_stmts()) == 1
    assert isinstance(stmt.else_branch, BasicBlock)
    assert len(stmt.else_branch.get_stmts()) == 1


def test_bool_str():
    """Test to string of bool literal renders inmanta true/false and not python
    """
    statements = parse_code(
        """
val1 = true
val2 = false
"""
    )
    assert len(statements) == 2
    assert isinstance(statements[0], Assign)
    assert isinstance(statements[1], Assign)
    assert str(statements[0].rhs) == "true"
    assert str(statements[1].rhs) == "false"


def test_1341_syntax_error_output_1():
    """
    Test the readability of a syntax error message.
    """
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
var=é,
)
            """
        )
    exc: ParserException = pytest_e.value
    assert exc.location.file == "test"
    assert exc.location.lnr == 2
    assert exc.location.start_char == 5
    assert exc.location.end_lnr == 2
    assert exc.location.end_char == 6
    assert exc.value == "é"
    assert exc.msg == "Syntax error: Illegal character 'é'"


def test_1341_syntax_error_output_2():
    """
    Test the readability of a syntax error message.
    """
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
deployment2 = k8s::Deployment(
    name="hello-nginx2",
    var=🤔,
    cluster=cluster
)
            """
        )
    exc: ParserException = pytest_e.value
    assert exc.location.file == "test"
    assert exc.location.lnr == 4
    assert exc.location.start_char == 9
    assert exc.location.end_lnr == 4
    assert exc.location.end_char == 10
    assert exc.value == "🤔"
    assert exc.msg == "Syntax error: Illegal character '🤔'"


def test_1341_syntax_error_output_3():
    """
    Test the readability of a syntax error message.
    """
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
é
            """
        )
    exc: ParserException = pytest_e.value
    assert exc.location.file == "test"
    assert exc.location.lnr == 2
    assert exc.location.start_char == 1
    assert exc.location.end_lnr == 2
    assert exc.location.end_char == 2
    assert exc.value == "é"
    assert exc.msg == "Syntax error: Illegal character 'é'"


def test_1341_syntax_error_output_4():
    """
    Test the readability of a syntax error message.
    """
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
aé=66
            """
        )
    exc: ParserException = pytest_e.value
    assert exc.location.file == "test"
    assert exc.location.lnr == 2
    assert exc.location.start_char == 2
    assert exc.location.end_lnr == 2
    assert exc.location.end_char == 3
    assert exc.value == "é"
    assert exc.msg == "Syntax error: Illegal character 'é'"


def test_1341_syntax_error_output_5():
    """
    Test the readability of a syntax error message.
    """
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
K8éééYamlResource.cluster [1] -- Cluster
            """
        )
    exc: ParserException = pytest_e.value
    assert exc.location.file == "test"
    assert exc.location.lnr == 2
    assert exc.location.start_char == 3
    assert exc.location.end_lnr == 2
    assert exc.location.end_char == 4
    assert exc.value == "é"
    assert exc.msg == "Syntax error: Illegal character 'é'"


def test_640_syntax_error_output_6():
    """
    Test the readability of a syntax error message.
    """
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
typedef positive as number matching self >= 1-
            """
        )
    exc: ParserException = pytest_e.value
    assert exc.location.file == "test"
    assert exc.location.lnr == 2
    assert exc.location.start_char == 46
    assert exc.location.end_lnr == 2
    assert exc.location.end_char == 47
    assert exc.value == "-"
    assert exc.msg == "Syntax error: Illegal character '-'"


def test_1766_empty_model_single_newline():
    statements = parse_code(
        """
        """
    )
    assert len(statements) == 0


def test_1766_empty_model_multiple_newline():
    statements = parse_code(
        """



        """
    )
    assert len(statements) == 0


def test_1707_out_of_place_regex():
    with pytest.raises(ParserException) as pytest_e:
        parse_code(
            """
/some_out_of_place_regex/
            """,
        )
    exc: ParserException = pytest_e.value
    assert exc.msg == "Syntax error at token /some_out_of_place_regex/"


def test_multiline_string_interpolation():
    statements = parse_code(
        """
str = \"\"\"
    var == {{var}}
\"\"\"
        """,
    )
    assert len(statements) == 1
    assert isinstance(statements[0], Assign)
    assert isinstance(statements[0].rhs, StringFormat)


def test_1804_bool_condition_as_bool():
    statements = parse_code(
        """
if false and true == true:
end
        """,
    )
    assert len(statements) == 1
    if_stmt = statements[0]
    assert isinstance(if_stmt, If)
    and_stmt = if_stmt.condition
    assert isinstance(and_stmt, And)
    assert len(and_stmt.children) == 2
    false_stmt = and_stmt.children[0]
    assert isinstance(false_stmt, Literal)
    assert isinstance(false_stmt.value, bool)
    assert false_stmt.value is False


def test_1573_condition_dict_lookup():
    statements = parse_code(
        """
dct = {"b": true}

if dct["b"]:
end
        """,
    )
    assert len(statements) == 2
    assert isinstance(statements[1], If)


@pytest.mark.parametrize(
    "expression,expected_tree",
    [
        ("42 == 42 and not false", (And, [(Equals, [(Literal, 42), (Literal, 42)]), (Not, [(Literal, False)])])),
        (
            "42 in [12, 42] or 'test' in []",
            (
                Or,
                [
                    (In, [(Literal, 42), (CreateList, [(Literal, 12), (Literal, 42)])]),
                    (In, [(Literal, "test"), (CreateList, [])]),
                ],
            ),
        ),
        ("not (42 in x)", (Not, [(In, [(Literal, 42), (Reference, "x")])])),
        ("not 42 in x", (Not, [(In, [(Literal, 42), (Reference, "x")])])),
        ("x or y.u is defined", (Or, [(Reference, "x"), (IsDefined, [(Reference, "y")])])),
    ],
)
def test_1815_conditional_expressions(expression, expected_tree):
    statements = parse_code(
        f"""
__x__ = {expression}
        """,
    )
    assert len(statements) == 1
    assign_stmt = statements[0]
    assert isinstance(assign_stmt, Assign)

    def expression_asserter(expression: ExpressionStatement, expected_tree):
        assert isinstance(expression, expected_tree[0])
        if isinstance(expression, Literal):
            assert expression.value == expected_tree[1]
        elif isinstance(expression, Reference):
            assert expression.name == expected_tree[1]
        elif isinstance(expression, ReferenceStatement):
            assert len(expression.children) == len(expected_tree[1])
            for child, child_expected in zip(expression.children, expected_tree[1]):
                if child_expected is None:
                    continue
                expression_asserter(child, child_expected)
        else:
            raise Exception("this test does not support %s" % type(expression))

    expression_asserter(assign_stmt.rhs, expected_tree)


def test_relation_deprecated_syntax():
    with warnings.catch_warnings(record=True) as w:
        parse_code(
            """
entity A:
end

entity B:
end

A aa [1] -- [0:] B bb
            """,
        )
        assert len(w) == 1
        assert issubclass(w[0].category, SyntaxDeprecationWarning)
        assert str(w[0].message) == (
            "The relation definition syntax `A aa [1:1] -- [0:] B bb` is deprecated."
            " Please use `A.bb [0:] -- B.aa [1:1]` instead. (test:8)"
        )
