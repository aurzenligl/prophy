#!/usr/bin/env python

from os.path import abspath, exists
from plyplus import Grammar, grammars

grammar_path = abspath('prophy.g')
g = Grammar(grammars.open(grammar_path))
out = g.parse(open('prophy.prophy').read())

from pprint import pprint
pprint(out.tail)

#import pdb;pdb.set_trace()

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
    print 'CONSTANT', str(tail[0].tail[0]), str(tail[1].tail[0])

def typedef_def(tail):
    print 'TYPEDEF', type_specifier(tail[0]), str(tail[1].tail[0])

def enum_def(tail):
    print 'ENUM', str(tail[0].tail[0]), ' '.join(
        str(x.tail[0].tail[0]) + '->' + str(x.tail[1].tail[0]) for x in tail[1].tail
    )

#def struct_def(tail):
#    print 'STRUCT', str(tail[0].tail[0]), ' '.join(
#        '{}->{}'.format(*declaration(x)) for x in tail[1].tail
#    )

defs = {
    'constant_def': constant_def,
    'typedef_def': typedef_def,
    'enum_def': enum_def,
#    'struct_def': struct_def
}

for x in out.tail:
    foo = defs.get(x.head)
    if foo:
        foo(x.tail)
