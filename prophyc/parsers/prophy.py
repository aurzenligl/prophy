import os
from collections import namedtuple

from plyplus import Grammar, grammars, ParseError

from prophyc.model import Constant, Typedef, Enum, EnumMember

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

builtins = {
    'u8', 'u16', 'u32', 'u64',
    'i8', 'i16', 'i32', 'i64',
    'float', 'double'
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

def type_specifier(tree):
    if tree.head in builtins:
        return str(tree.head)
    else:
        return str(tree.tail[0])

def declaration(tree):
    return type_specifier(tree.tail[0]), str(tree.tail[1].tail[0])

def constant_def(state, tail):
    name = str(tail[0].tail[0])
    value = str(tail[1].tail[0])

    validate_decl_not_defined(state, name)

    node = Constant(name, value)
    state.constdecls[name] = node
    return node

def typedef_def(state, tail):
    type_ = type_specifier(tail[0])
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

    enumerators = [enumerator_def(tree) for tree in tail[1].tail]

    node = Enum(name, enumerators)
    state.typedecls[name] = node
    return node

#def struct_def(tail):
#    print 'STRUCT', str(tail[0].tail[0]), ' '.join(
#        '{}->{}'.format(*declaration(x)) for x in tail[1].tail
#    )

symbols = {
    'constant_def': constant_def,
    'typedef_def': typedef_def,
    'enum_def': enum_def,
#    'struct_def': struct_def
}

_grammar = None

def get_grammar():
    global _grammar
    if not _grammar:
        grammar_path = os.path.join(os.path.split(__file__)[0], 'prophy.g')
        _grammar = Grammar(grammars.open(grammar_path))
    return _grammar

def build_model(string_):
    out = get_grammar().parse(string_)
    state = State({}, {})
    return [symbols[tree.head](state, tree.tail) for tree in out.tail]

class ProphyParser(object):

    def parse_string(self, string_):
        return build_model(string_)
