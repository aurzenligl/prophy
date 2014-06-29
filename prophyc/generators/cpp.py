import os

from prophyc import model
from prophyc import model_process

primitive_types = {
    'u8': 'uint8_t',
    'u16': 'uint16_t',
    'u32': 'uint32_t',
    'u64': 'uint64_t',
    'i8': 'int8_t',
    'i16': 'int16_t',
    'i32': 'int32_t',
    'i64': 'int64_t',
    'r32': 'float',
    'r64': 'double',
    'byte': 'uint8_t',
}

def _indent(string_, spaces):
    indentation = spaces * ' '
    return indentation + ('\n' + indentation).join(string_.split('\n'))

def _generate_include(pnodes, include):
    return '#include "{}.hpp"'.format(include.name)

def _generate_constant(pnodes, constant):
    return 'enum {{ {} = {} }};'.format(constant.name, constant.value)

def _generate_typedef(pnodes, typedef):
    return 'typedef {} {};'.format(typedef.type, typedef.name)

def _generate_enum(pnodes, enum):
    members = ',\n'.join('    {} = {}'.format(name, value)
                         for name, value in enum.members)
    return 'enum {}\n{{\n{}\n}};'.format(enum.name, members)

def _generate_struct(pnodes, struct):
    def gen_member(member):
        def build_annotation(member):
            if member.array_size:
                if member.array_bound:
                    annotation = 'limited array, size in {}'.format(member.array_bound)
                else:
                    annotation = ''
            else:
                if member.array_bound:
                    annotation = 'dynamic array, size in {}'.format(member.array_bound)
                else:
                    annotation = 'greedy array'
            return annotation

        typename = primitive_types.get(member.type, member.type)
        if member.array:
            annotation = build_annotation(member)
            size = member.array_size or 1
            if annotation:
                return '    {} {}[{}]; /// {}\n'.format(typename, member.name, size, annotation)
            else:
                return '    {} {}[{}];\n'.format(typename, member.name, size)
        return '    {} {};\n'.format(typename, member.name)
    def gen_part(i, part):
        generated = 'struct part{0}\n{{\n{1}}} _{0};'.format(
            i + 2,
            ''.join(map(gen_member, part))
        )
        return _indent(generated, 4)

    main, parts = pnodes.partition(struct.members)
    generated = ''.join(map(gen_member, main))
    if parts:
        generated += '\n' + '\n\n'.join(map(gen_part, range(len(parts)), parts)) + '\n'

    return 'struct {}\n{{\n{}}};'.format(struct.name, generated)

_generate_visitor = {
    model.Include: _generate_include,
    model.Constant: _generate_constant,
    model.Typedef: _generate_typedef,
    model.Enum: _generate_enum,
    model.Struct: _generate_struct,
#    model.Union: _generate_union
}

def _generate(pnodes, node):
    return _generate_visitor[type(node)](pnodes, node)

def _generator(nodes):
    pnodes = model_process.ProcessedNodes(nodes)
    last_node = None
    for node in nodes:
        prepend_newline = bool(last_node
                               and (isinstance(last_node, (model.Enum, model.Struct, model.Union))
                                    or type(last_node) is not type(node)))
        yield prepend_newline * '\n' + _generate(pnodes, node) + '\n'
        last_node = node

header = """\
#ifndef _PROPHY_GENERATED_{0}_HPP
#define _PROPHY_GENERATED_{0}_HPP

#include <prophy/prophy.hpp>
"""

footer = """\
#endif  /* _PROPHY_GENERATED_{0}_HPP */
"""

class CppGenerator(object):

    def __init__(self, output_dir = "."):
        self.output_dir = output_dir

    def generate_definitions(self, nodes):
        return ''.join(_generator(nodes))

    def serialize_string(self, nodes, basename):
        return '\n'.join((
            header.format(basename),
            self.generate_definitions(nodes),
            footer.format(basename)
        ))

    def serialize(self, nodes, basename):
        path = os.path.join(self.output_dir, basename + ".hpp")
        out = self.serialize_string(nodes, basename)
        open(path, "w").write(out)
