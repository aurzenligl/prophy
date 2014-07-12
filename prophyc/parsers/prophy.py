#!/usr/bin/env python

import os

from plyplus import Grammar, grammars, ParseError

from prophyc.model import Constant, Typedef

builtins = {
    'u8', 'u16', 'u32', 'u64',
    'i8', 'i16', 'i32', 'i64',
    'float', 'double'
}

def type_specifier(tree):
    if tree.head in builtins:
        return str(tree.head)
    else:
        return str(tree.tail[0])

def declaration(tree):
    return type_specifier(tree.tail[0]), str(tree.tail[1].tail[0])

def constant_def(tail):
    return Constant(str(tail[0].tail[0]), str(tail[1].tail[0]))

def typedef_def(tail):
    return Typedef(type_specifier(tail[0]), str(tail[1].tail[0]))

def enum_def(tail):
    print 'ENUM', str(tail[0].tail[0]), ' '.join(
        str(x.tail[0].tail[0]) + '->' + str(x.tail[1].tail[0]) for x in tail[1].tail
    )

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
    return [symbols[tree.head](tree.tail) for tree in out.tail]

class ProphyParser(object):

    def parse_string(self, string_):
        return build_model(string_)
