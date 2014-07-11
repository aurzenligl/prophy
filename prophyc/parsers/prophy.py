#!/usr/bin/env python

from os.path import abspath, exists
from plyplus import Grammar, grammars

grammar_path = abspath('prophy.g')
g = Grammar(grammars.open(grammar_path))
out = g.parse(open('prophy.prophy').read())

from pprint import pprint
pprint(out.tail)
