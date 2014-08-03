import os
from collections import namedtuple

from plyplus import Grammar, grammars, ParseError

from prophyc.model import Constant, Typedef, Enum, EnumMember, Struct, StructMember, Union, UnionMember

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

builtins = {
    'u8': 'u8',
    'u16': 'u16',
    'u32': 'u32',
    'u64': 'u64',
    'i8': 'i8',
    'i16': 'i16',
    'i32': 'i32',
    'i64': 'i64',
    'float': 'r32',
    'r32': 'r32',
    'double': 'r64',
    'r64': 'r64',
    'byte': 'byte'
}

State = namedtuple('State', ['typedecls', 'constdecls'])

def validate_decl_not_defined(state, name):
    if name in state.typedecls or name in state.constdecls:
        raise Exception("Name '{}' redefined".format(name))

def validate_typedecl_exists(state, type_):
    if type_ not in builtins and type_ not in state.typedecls:
        raise Exception("Type '{}' was not declared".format(type_))

def validate_constdecl_exists(state, value):
    if not _is_int(value) and value not in state.constdecls:
        raise Exception("Constant '{}' was not declared".format(value))

def validate_value_positive(state, value):
    if _is_int(value) and int(value) <= 0:
        raise Exception("Array size '{}' must be positive".format(value))

def validate_field_name_not_defined(names, name):
    if name in names:
        raise Exception("Field '{}' redefined".format(name))

def validate_value_not_defined(values, value):
    if value in values:
        raise Exception("Value '{}' redefined".format(value))

def validate_greedy_field_last(last_index, index, name):
    if index != last_index:
        raise Exception("Greedy array field '{}' not last".format(name))

def get_type_specifier(tree):
    return builtins.get(tree.head, str(tree.tail[0]))

def get_struct_type_specifier(tree):
    if tree.head == 'bytes':
        return 'byte'
    else:
        return get_type_specifier(tree)

def constant_def(state, tail):
    name = str(tail[0].tail[0])
    value = str(tail[1].tail[0])
    validate_decl_not_defined(state, name)

    node = Constant(name, value)
    state.constdecls[name] = node
    return node

def typedef_def(state, tail):
    type_ = get_type_specifier(tail[0])
    name = str(tail[1].tail[0])
    validate_decl_not_defined(state, name)
    validate_typedecl_exists(state, type_)

    node = Typedef(name, type_)
    state.typedecls[name] = node
    return node

def enum_def(state, tail):
    def enumerator_def(tree):
        name = str(tree.tail[0].tail[0])
        value = str(tree.tail[1].tail[0])
        validate_decl_not_defined(state, name)
        validate_constdecl_exists(state, value)

        member = EnumMember(name, value)
        state.constdecls[name] = member
        return member

    name = str(tail[0].tail[0])
    validate_decl_not_defined(state, name)

    node = Enum(name, [enumerator_def(tree) for tree in tail[1].tail])
    state.typedecls[name] = node
    return node

def struct_def(state, tail):
    def field_def(tail):
        names = set()
        last_index = len(tail) - 1
        for index, tree in enumerate(tail):
            type_ = get_struct_type_specifier(tree.tail[0])
            if tree.tail[1].head == 'optional':
                optional = True
                name = str(tree.tail[2].tail[0])
            else:
                optional = False
                name = str(tree.tail[1].tail[0])

            validate_field_name_not_defined(names, name)
            validate_typedecl_exists(state, type_)
            names.add(name)

            if len(tree.tail) > 2 and not optional:
                array = tree.tail[2]
                if array.head == 'fixed_array':
                    value = str(array.tail[0].tail[0])
                    validate_constdecl_exists(state, value)
                    validate_value_positive(state, value)
                    yield StructMember(name, type_, True, None, value, False)
                elif array.head == 'dynamic_array':
                    yield StructMember('num_of_' + name, 'u32', None, None, None, False)
                    yield StructMember(name, type_, True, 'num_of_' + name, None, False)
                elif array.head == 'limited_array':
                    value = str(array.tail[0].tail[0])
                    validate_constdecl_exists(state, value)
                    validate_value_positive(state, value)
                    yield StructMember('num_of_' + name, 'u32', None, None, None, False)
                    yield StructMember(name, type_, True, 'num_of_' + name, value, False)
                else:
                    validate_greedy_field_last(last_index, index, name)
                    yield StructMember(name, type_, True, None, None, False)
            else:
                yield StructMember(name, type_, None, None, None, optional)

    name = str(tail[0].tail[0])
    validate_decl_not_defined(state, name)

    node = Struct(name, [x for x in field_def(tail[1].tail)])
    state.typedecls[name] = node
    return node

def union_def(state, tail):
    def arm_def(tree, names = set(), values = set()):
        value = str(tree.tail[0].tail[0])
        type_ = get_type_specifier(tree.tail[1])
        name = str(tree.tail[2].tail[0])
        validate_typedecl_exists(state, type_)
        validate_constdecl_exists(state, value)
        validate_field_name_not_defined(names, name)
        validate_value_not_defined(values, value)
        values.add(value)
        names.add(name)
        return UnionMember(name, type_, value)

    name = str(tail[0].tail[0])
    validate_decl_not_defined(state, name)

    node = Union(name, [arm_def(x) for x in tail[1].tail])
    state.typedecls[name] = node
    return node

symbols = {
    'constant_def': constant_def,
    'typedef_def': typedef_def,
    'enum_def': enum_def,
    'struct_def': struct_def,
    'union_def': union_def
}

_grammar = None

def get_grammar():
    global _grammar
    if not _grammar:
        grammar_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'prophy.g')
        _grammar = Grammar(grammars.open(grammar_path))
    return _grammar

def build_model(string_):
    out = get_grammar().parse(string_)
    state = State({}, {})
    return [symbols[tree.head](state, tree.tail) for tree in out.tail]

class ProphyParser(object):

    def parse_string(self, string_):
        return build_model(string_)

    def parse(self, filename):
        return build_model(open(filename).read())
