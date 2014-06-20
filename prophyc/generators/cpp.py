import os

from prophyc import model

def _generate_include(include):
    return '#include "{0}.hpp"'.format(include.name)

def _generate_typedef(typedef):
    return 'typedef {0} {1};'.format(typedef.type, typedef.name)

_generate_visitor = {
    model.Include: _generate_include,
#    model.Constant: _generate_constant,
    model.Typedef: _generate_typedef,
#    model.Enum: _generate_enum,
#    model.Struct: _generate_struct,
#    model.Union: _generate_union
}

def _generate(node):
    return _generate_visitor[type(node)](node)

def _generator(nodes):
    last_node = None
    for node in nodes:
        prepend_newline = bool(last_node and type(node) is not type(last_node))
        yield prepend_newline * '\n' + _generate(node) + '\n'
        last_node = node

class CppGenerator(object):

    def generate_definitions(self, nodes):
        return ''.join(_generator(nodes))
