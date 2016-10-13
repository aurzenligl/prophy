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

def _indent(string_, spaces):
    indentation = spaces * ' '
    return '\n'.join(indentation + x if x else x for x in string_.split('\n'))

def _to_literal(value):
    try:
        return '{}{}'.format(value, int(value, 0) > 0 and 'u' or '')
    except ValueError:
        return value

def _generate_def_include(include):
    return '#include "{}.pp.hpp"'.format(include.name)

def _generate_def_constant(constant):
    return 'enum {{ {} = {} }};'.format(constant.name, _to_literal(constant.value))

def _generate_def_typedef(typedef):
    tp = primitive_types.get(typedef.type_, typedef.type_)
    return 'typedef {} {};'.format(tp, typedef.name)

def _generate_def_enum(enum):
    members = ',\n'.join('{} = {}'.format(member.name, _to_literal(member.value))
                         for member in enum.members)
    return 'enum {}\n{{\n{}\n}};'.format(enum.name, _indent(members, 4))

def _generate_def_struct(struct):
    def gen_member(member):
        def build_annotation(member):
            if member.size:
                if member.bound:
                    annotation = 'limited array, size in {}'.format(member.bound)
                else:
                    annotation = ''
            else:
                if member.bound:
                    annotation = 'dynamic array, size in {}'.format(member.bound)
                else:
                    annotation = 'greedy array'
            return annotation

        typename = primitive_types.get(member.type_, member.type_)
        if member.array:
            annotation = build_annotation(member)
            size = member.size or 1
            if annotation:
                field = '{0} {1}[{2}]; /// {3}\n'.format(typename, member.name, size, annotation)
            else:
                field = '{0} {1}[{2}];\n'.format(typename, member.name, size)
        else:
            field = '{0} {1};\n'.format(typename, member.name)
        if member.optional:
            return 'prophy::bool_t has_{0};\n'.format(member.name) + field
        return field

    def gen_part(i, part):
        generated = 'struct part{0}\n{{\n{1}}} _{0};'.format(
            i + 2,
            _indent(''.join(map(gen_member, part)), 4)
        )
        return _indent(generated, 4)

    main, parts = model.partition(struct.members)
    generated = _indent(''.join(map(gen_member, main)), 4)
    if parts:
        generated += '\n' + '\n\n'.join(map(gen_part, range(len(parts)), parts)) + '\n'

    return 'struct {}\n{{\n{}}};'.format(struct.name, generated)

def _generate_def_union(union):
    def gen_member(member):
        typename = primitive_types.get(member.type_, member.type_)
        return '{0} {1};\n'.format(typename, member.name)

    enum_fields = ',\n'.join('discriminator_{0} = {1}'.format(mem.name,
                                                              mem.discriminator)
                             for mem in union.members)
    union_fields = ''.join(map(gen_member, union.members))
    enum_def = 'enum _discriminator\n{{\n{0}\n}} discriminator;'.format(_indent(enum_fields, 4))
    union_def = 'union\n{{\n{0}}};'.format(_indent(union_fields, 4))
    return 'struct {0}\n{{\n{1}\n\n{2}\n}};'.format(union.name,
                                                    _indent(enum_def, 4),
                                                    _indent(union_def, 4))

_generate_def_visitor = {
    model.Include: _generate_def_include,
    model.Constant: _generate_def_constant,
    model.Typedef: _generate_def_typedef,
    model.Enum: _generate_def_enum,
    model.Struct: _generate_def_struct,
    model.Union: _generate_def_union
}

def _generator_def(nodes):
    last_node = None
    for node in nodes:
        prepend_newline = bool(last_node
                               and (isinstance(last_node, (model.Enum, model.Struct, model.Union))
                                    or type(last_node) is not type(node)))
        yield prepend_newline * '\n' + _generate_def_visitor[type(node)](node) + '\n'
        last_node = node

def _member_access_statement(member):
    out = '&payload->%s' % member.name
    if isinstance(member, model.StructMember) and member.array:
        out = out[1:]
    return out

def _generate_swap_struct(struct):
    def gen_member(member, delimiters = []):
        if member.array:
            is_dynamic = member.kind == model.Kind.DYNAMIC
            swap_mode = 'dynamic' if is_dynamic else 'fixed'
            if member.bound:
                bound = member.bound
                if member.bound not in delimiters:
                    bound = 'payload->' + bound
                return 'swap_n_{0}({1}, {2})'.format(
                    swap_mode, _member_access_statement(member), bound)
            elif not member.bound and member.size:
                return 'swap_n_{0}({1}, {2})'.format(
                    swap_mode, _member_access_statement(member), member.size)
        else:
            if member.optional:
                preamble = 'swap(&payload->has_{0});\nif (payload->has_{0}) '.format(member.name)
            else:
                preamble = ''
            return preamble + 'swap({0})'.format(_member_access_statement(member))

    def gen_last_member(name, last_mem, delimiters = []):
        if last_mem.kind == model.Kind.UNLIMITED or last_mem.greedy:
            return 'return cast<{0}*>({1});\n'.format(
                name,
                _member_access_statement(last_mem)
            )
        elif last_mem.kind == model.Kind.DYNAMIC or last_mem.dynamic:
            return 'return cast<{0}*>({1});\n'.format(
                name,
                gen_member(last_mem, delimiters)
            )
        else:
            return gen_member(last_mem) + ';\n' + 'return payload + 1;\n'

    def gen_main(main, parts):
        all_names = {mem.name: 'payload' for mem in main}
        for i, part in enumerate(parts):
            all_names.update({mem.name: 'part{0}'.format(i + 2) for mem in part})

        def get_missing(part_number):
            part = parts[part_number]
            names = [mem.name for mem in part]
            return [(all_names[mem.bound], mem.bound)
                    for mem in part
                    if mem.bound and mem.bound not in names]

        def gen_missing(part_number):
            return ''.join(', {0}->{1}'.format(x[0], x[1]) for x in get_missing(part_number))

        members = ''.join(gen_member(mem) + ';\n' for mem in main[:-1])
        if parts:
            for i, part in enumerate(parts):
                members += '{0}::part{1}* part{1} = cast<{0}::part{1}*>({2});\n'.format(
                    struct.name,
                    i + 2,
                    'swap(part{0}{1})'.format(i + 1, gen_missing(i - 1)) if i else gen_member(main[-1])
                )
            members += 'return cast<{0}*>(swap(part{1}{2}));\n'.format(struct.name, i + 2, gen_missing(i))
        elif main:
            members += gen_last_member(struct.name, main[-1])
        else:
            members += 'return payload + 1;\n'
        return ('template <>\n'
                '{0}* swap<{0}>({0}* payload)\n'
                '{{\n'
                '{1}'
                '}}\n').format(struct.name, _indent(members, 4))

    def gen_part(part_number, part):
        names = [mem.name for mem in part]
        delimiters = [mem.bound for mem in part if mem.bound and mem.bound not in names]
        members = ''.join(gen_member(mem, delimiters) + ';\n' for mem in part[:-1])
        members += gen_last_member(struct.name + '::part{0}'.format(part_number), part[-1], delimiters)
        return ('inline {0}::part{1}* swap({0}::part{1}* payload{3})\n'
                '{{\n'
                '{2}}}\n').format(struct.name,
                                  part_number,
                                  _indent(members, 4),
                                  ''.join(', size_t {0}'.format(x) for x in delimiters))

    main, parts = model.partition(struct.members)
    return '\n'.join([gen_part(i + 2, part) for i, part in enumerate(parts)] +
                     [gen_main(main, parts)])

def _generate_swap_union(union):
    return ('template <>\n'
            '{0}* swap<{0}>({0}* payload)\n'
            '{{\n'
            '    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));\n'
            '    switch (payload->discriminator)\n'
            '    {{\n{1}'
            '        default: break;\n'
            '    }}\n'
            '    return payload + 1;\n'
            '}}\n').format(
                union.name,
                ''.join(8 * ' ' + 'case {0}::discriminator_{1}: swap({2}); break;\n'.format(
                    union.name, m.name, _member_access_statement(m)
                ) for m in union.members)
            )

_generate_swap_visitor = {
    model.Struct: _generate_swap_struct,
    model.Union: _generate_swap_union
}

def _generator_swap(nodes):
    for node in nodes:
        fun = _generate_swap_visitor.get(type(node))
        if fun:
            yield fun(node)

header = """\
#ifndef _PROPHY_GENERATED_{0}_HPP
#define _PROPHY_GENERATED_{0}_HPP

#include <prophy/prophy.hpp>
"""

footer = """\
#endif  /* _PROPHY_GENERATED_{0}_HPP */
"""

swap_header = """\
namespace prophy
{
"""

swap_footer = """\
} // namespace prophy
"""

class CppGenerator(object):

    def __init__(self, output_dir = "."):
        self.output_dir = output_dir

    def generate_definitions(self, nodes):
        return ''.join(_generator_def(nodes))

    def generate_swap_declarations(self, nodes):
        out = ''.join(
            'template <> inline {0}* swap<{0}>({0}* in) {{ swap(reinterpret_cast<uint32_t*>(in)); return in + 1; }}\n'
            .format(node.name)
            for node in nodes
            if isinstance(node, (model.Enum))
        )
        out += ''.join(
            'template <> {0}* swap<{0}>({0}*);\n'.format(node.name)
            for node in nodes
            if isinstance(node, (model.Struct, model.Union))
        )
        return out.join((
            'namespace prophy\n'
            '{\n'
            '\n',
            '\n'
            '} // namespace prophy\n'
        ))

    def generate_swap(self, nodes):
        return '\n'.join(_generator_swap(nodes))

    def serialize_string_hpp(self, nodes, basename):
        return '\n'.join((
            header.format(basename),
            self.generate_definitions(nodes),
            self.generate_swap_declarations(nodes),
            footer.format(basename)
        ))

    def serialize_string_cpp(self, nodes, basename):
        return '\n'.join((
            '#include <prophy/detail/prophy.hpp>\n',
            '#include "{0}.pp.hpp"\n'.format(basename),
            'using namespace prophy::detail;\n',
            swap_header,
            self.generate_swap(nodes),
            swap_footer
        ))

    def serialize(self, nodes, basename):
        hpp_path = os.path.join(self.output_dir, basename + ".pp.hpp")
        cpp_path = os.path.join(self.output_dir, basename + ".pp.cpp")
        open(hpp_path, "w").write(self.serialize_string_hpp(nodes, basename))
        open(cpp_path, "w").write(self.serialize_string_cpp(nodes, basename))
