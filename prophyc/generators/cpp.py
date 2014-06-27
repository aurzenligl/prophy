import os

from prophyc import model

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

def _generate_include(include):
    return '#include "{}.hpp"'.format(include.name)

def _generate_constant(constant):
    return 'enum {{ {} = {} }};'.format(constant.name, constant.value)

def _generate_typedef(typedef):
    return 'typedef {} {};'.format(typedef.type, typedef.name)

def _generate_enum(enum):
    members = ',\n'.join('    {} = {}'.format(name, value)
                         for name, value in enum.members)
    return 'enum {}\n{{\n{}\n}};'.format(enum.name, members)

def _generate_struct(struct):
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

    members = ''.join(map(gen_member, struct.members))
    return 'struct {}\n{{\n{}}};'.format(struct.name, members)

_generate_visitor = {
    model.Include: _generate_include,
    model.Constant: _generate_constant,
    model.Typedef: _generate_typedef,
    model.Enum: _generate_enum,
    model.Struct: _generate_struct,
#    model.Union: _generate_union
}

def _generate(node):
    return _generate_visitor[type(node)](node)

def _generator(nodes):
    last_node = None
    for node in nodes:
        prepend_newline = bool(last_node
                               and (isinstance(last_node, (model.Enum, model.Struct, model.Union))
                                    or type(last_node) is not type(node)))
        yield prepend_newline * '\n' + _generate(node) + '\n'
        last_node = node

class CppGenerator(object):

    def generate_definitions(self, nodes):
        return ''.join(_generator(nodes))
