from prophyc import model
from prophyc.model import DISC_SIZE, BUILTIN_SIZES

BUILTIN2C = {
    'i8': 'int8_t',
    'i16': 'int16_t',
    'i32': 'int32_t',
    'i64': 'int64_t',
    'u8': 'uint8_t',
    'u16': 'uint16_t',
    'u32': 'uint32_t',
    'u64': 'uint64_t',
    'byte': 'uint8_t',
    'r32': 'float',
    'r64': 'double'
}

def _indent(text):
    return '\n'.join(x and '    ' + x or '' for x in text.split('\n'))

def generate_include_definition(node):
    return '#include "{0}.ppf.hpp"\n'.format(node.name)

def generate_constant_definition(node):
    return 'enum {{ {0} = {1} }};\n'.format(node.name, node.value)

def generate_enum_definition(node):
    body = ',\n'.join('    {0} = {1}'.format(m.name, m.value) for m in node.members) + '\n'
    return 'enum {0}\n'.format(node.name) + '{\n' + body + '};\n'

def generate_typedef_definition(node):
    return 'typedef {0} {1};\n'.format(BUILTIN2C.get(node.type, node.type), node.name)

def generate_struct_definition(node):
    constructor = generate_struct_constructor(node)
    if constructor:
        constructor = '{0}(): {1} {{ }}\n'.format(node.name, constructor)
    return (
        'struct {0} : prophy::detail::message<{0}>\n'.format(node.name)
        + '{\n'
        + _indent(
            '\n'.join(x for x in (
                'enum {{ encoded_byte_size = {0} }};\n'.format(generate_struct_encoded_byte_size(node)),
                generate_struct_fields(node),
                constructor,
                'size_t get_byte_size() const\n'
                + '{\n'
                + _indent(generate_struct_get_byte_size(node))
                + '}\n'
            ) if x)
        )
        + '};\n'
    )

def generate_union_definition(node):
    return (
        'struct {0} : prophy::detail::message<{0}>\n'.format(node.name)
        + '{\n'
        + _indent(
            '\n'.join((
                'enum {{ encoded_byte_size = {0} }};\n'.format(generate_union_encoded_byte_size(node)),
                generate_union_fields(node),
                '{0}(): {1} {{ }}\n'.format(node.name, generate_union_constructor(node)),
                'size_t get_byte_size() const\n'
                + '{\n'
                + _indent(generate_union_get_byte_size(node))
                + '}\n'
            ))
        )
        + '};\n'
    )

def generate_enum_implementation(node):
    return (
        'template <>\n'
        + 'const char* print_traits<{0}>::to_literal({0} x)\n'.format(node.name)
        + '{\n'
        + _indent(
            'switch (x)\n'
            + '{\n'
            + _indent(
                ''.join('case {0}: return "{0}";\n'.format(m.name) for m in node.members)
                + 'default: return 0;\n'
            )
            + '}\n'
        )
        + '}\n'
    )

def generate_struct_implementation(node):
    def encode_impl(node):
        return (
            'template <>\n'
            + 'template <endianness E>\n'
            + 'uint8_t* message_impl<{0}>::encode(const {0}& x, uint8_t* pos)\n'.format(node.name)
            + '{\n'
            + _indent(
                generate_struct_encode(node)
                + 'return pos;\n'
            )
            + '}\n'
            + ''.join(
                'template uint8_t* message_impl<{0}>::encode<{1}>(const {0}& x, uint8_t* pos);\n'.format(node.name, e)
                for e in ('native', 'little', 'big')
            )
        )
    def decode_impl(node):
        return (
            'template <>\n'
            + 'template <endianness E>\n'
            + 'bool message_impl<{0}>::decode({0}& x, const uint8_t*& pos, const uint8_t* end)\n'.format(node.name)
            + '{\n'
            + _indent(
                'return (\n'
                + _indent(generate_struct_decode(node))
                + ');\n'
            )
            + '}\n'
            + ''.join(
                'template bool message_impl<{0}>::decode<{1}>({0}& x, const uint8_t*& pos, const uint8_t* end);\n'.format(node.name, e)
                for e in ('native', 'little', 'big')
            )
        )
    def print_impl(node):
        return (
            'template <>\n'
            + 'void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent)\n'.format(node.name)
            + '{\n'
            + _indent(generate_struct_print(node))
            + '}\n'
            + 'template void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent);\n'.format(node.name)
        )
    return (
        encode_impl(node) + '\n'
        + decode_impl(node) + '\n'
        + print_impl(node)        
    )

def generate_union_implementation(node):
    def encode_impl(node):
        return (
            'template <>\n'
            + 'template <endianness E>\n'
            + 'uint8_t* message_impl<{0}>::encode(const {0}& x, uint8_t* pos)\n'.format(node.name)
            + '{\n'
            + _indent(
                generate_union_encode(node)
                + 'return pos;\n'
            )
            + '}\n'
            + ''.join(
                'template uint8_t* message_impl<{0}>::encode<{1}>(const {0}& x, uint8_t* pos);\n'.format(node.name, e)
                for e in ('native', 'little', 'big')
            )
        )
    def decode_impl(node):
        return (
            'template <>\n'
            + 'template <endianness E>\n'
            + 'bool message_impl<{0}>::decode({0}& x, const uint8_t*& pos, const uint8_t* end)\n'.format(node.name)
            + '{\n'
            + _indent(generate_union_decode(node))
            + '}\n'
            + ''.join(
                'template bool message_impl<{0}>::decode<{1}>({0}& x, const uint8_t*& pos, const uint8_t* end);\n'.format(node.name, e)
                for e in ('native', 'little', 'big')
            )
        )
    def print_impl(node):
        return (
            'template <>\n'
            + 'void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent)\n'.format(node.name)
            + '{\n'
            + _indent(generate_union_print(node))
            + '}\n'
            + 'template void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent);\n'.format(node.name)
        )
    return (
        encode_impl(node) + '\n'
        + decode_impl(node) + '\n'
        + print_impl(node)
    )

def generate_struct_encode(node):
    text = ''
    bound = {m.bound:m for m in node.members if m.bound}
    delimiters = {bound[m.name].name:m for m in node.members if m.name in bound}
    for m in node.members:
        if m.fixed:
            text += 'pos = do_encode<E>(pos, x.{0}, {1});\n'.format(m.name, m.size)
        elif m.dynamic:
            d = delimiters[m.name]
            text += 'pos = do_encode<E>(pos, x.{0}.data(), {1}(x.{0}.size()));\n'.format(m.name, BUILTIN2C[d.type])
        elif m.limited:
            d = delimiters[m.name]
            text += (
                'do_encode<E>(pos, x.{0}.data(), {2}(std::min(x.{0}.size(), size_t({1}))));\n'.format(m.name, m.size, BUILTIN2C[d.type])
                + 'pos = pos + {0};\n'.format(m.byte_size)
            )
        elif m.greedy:
            text += 'pos = do_encode<E>(pos, x.{0}.data(), x.{0}.size());\n'.format(m.name)
        elif m.optional:
            discpad = (m.alignment > DISC_SIZE) and (m.alignment - DISC_SIZE) or 0
            discpadtext = discpad and 'pos = pos + {0};\n'.format(discpad) or ''
            text += (
                'pos = do_encode<E>(pos, x.has_{0});\n'.format(m.name)
                + discpadtext
                + 'if (x.has_{0}) do_encode<E>(pos, x.{0});\n'.format(m.name)
                + 'pos = pos + {0};\n'.format(m.byte_size - DISC_SIZE - discpad)
            )
        elif m.name in bound:
            b = bound[m.name]
            if b.dynamic:
                text += 'pos = do_encode<E>(pos, {1}(x.{0}.size()));\n'.format(b.name, BUILTIN2C[m.type])
            else:
                text += (
                    'pos = do_encode<E>(pos, {2}(std::min(x.{0}.size(), size_t({1}))));\n'
                    .format(b.name, b.size, BUILTIN2C[m.type])
                )
        else:
            text += 'pos = do_encode<E>(pos, x.{0});\n'.format(m.name)
        if m.padding:
            if m.padding < 0:
                text += 'pos = align<{0}>(pos);\n'.format(abs(m.padding))
            else:
                text += 'pos = pos + {0};\n'.format(m.padding)
    return text

def generate_struct_decode(node):
    text = []
    bound = {m.bound:m for m in node.members if m.bound}
    for m in node.members:
        if m.fixed:
            text.append('do_decode<E>(x.{0}, {1}, pos, end)'.format(m.name, m.size))
        elif m.dynamic:
            text.append('do_decode<E>(x.{0}.data(), x.{0}.size(), pos, end)'.format(m.name))
        elif m.limited:
            text.append('do_decode_in_place<E>(x.{0}.data(), x.{0}.size(), pos, end)'.format(m.name))
            text.append('do_decode_advance({0}, pos, end)'.format(m.byte_size))
        elif m.greedy:
            text.append('do_decode_greedy<E>(x.{0}, pos, end)'.format(m.name))
        elif m.optional:
            discpad = (m.alignment > DISC_SIZE) and (m.alignment - DISC_SIZE) or 0
            text.append('do_decode<E>(x.has_{0}, pos, end)'.format(m.name))
            if discpad:
                text.append('do_decode_advance({0}, pos, end)'.format(discpad))
            text.append('do_decode_in_place_optional<E>(x.{0}, x.has_{0}, pos, end)'.format(m.name))
            text.append('do_decode_advance({0}, pos, end)'.format(m.byte_size - DISC_SIZE - discpad))
        elif m.name in bound:
            b = bound[m.name]
            if b.dynamic:
                text.append('do_decode_resize<E, {1}>(x.{0}, pos, end)'.format(b.name, BUILTIN2C[m.type]))
            else:
                text.append('do_decode_resize<E, {2}>(x.{0}, pos, end, {1})'.format(b.name, b.size, BUILTIN2C[m.type]))
        else:
            text.append('do_decode<E>(x.{0}, pos, end)'.format(m.name))
        if m.padding:
            if m.padding < 0:
                text.append('do_decode_align<{0}>(pos, end)'.format(abs(m.padding)))
            else:
                text.append('do_decode_advance({0}, pos, end)'.format(m.padding))
    return ' &&\n'.join(text) + '\n'

def generate_struct_print(node):
    text = ''
    bound = {m.bound:m for m in node.members if m.bound}
    for m in node.members:
        if m.array:
            if m.fixed:
                inner = 'x.{0}, size_t({1})'.format(m.name, m.size)
            elif m.dynamic:
                inner = 'x.{0}.data(), x.{0}.size()'.format(m.name)
            elif m.limited:
                inner = 'x.{0}.data(), std::min(x.{0}.size(), size_t({1}))'.format(m.name, m.size)
            elif m.greedy:
                inner = 'x.{0}.data(), x.{0}.size()'.format(m.name)
            if m.type == 'byte':
                inner = inner.join(('std::make_pair(', ')'))
            text += 'do_print(out, indent, "{0}", {1});\n'.format(m.name, inner)
        elif m.optional:
            text += 'if (x.has_{0}) do_print(out, indent, "{0}", x.{0});\n'.format(m.name)
        elif m.name in bound:
            pass
        else:
            text += 'do_print(out, indent, "{0}", x.{0});\n'.format(m.name)
    return text

def generate_struct_encoded_byte_size(node):
    return (node.kind == model.Kind.FIXED) and str(node.byte_size) or '-1'

def generate_struct_get_byte_size(node):
    def byte_size(m):
        return BUILTIN_SIZES.get(m.type) or DISC_SIZE * isinstance(m.definition, model.Enum) or m.definition.byte_size
    bytes = 0
    elems = []
    for m in node.members:
        if m.kind == model.Kind.FIXED:
            if m.dynamic or m.greedy:
                elems += ['{0}.size() * {1}'.format(m.name, byte_size(m))]
            else:
                bytes += m.byte_size + m.padding
        else:
            if m.dynamic or m.greedy:
                elems += ['std::accumulate({0}.begin(), {0}.end(), size_t(), prophy::detail::byte_size())'.format(m.name)]
            else:
                elems += ['{0}.get_byte_size()'.format(m.name)]
        if m.padding < 0:
            if bytes:
                elems += [str(bytes)]
                bytes = 0
            elems = [
                'prophy::detail::nearest<{0}>(\n'.format(abs(m.padding))
                + _indent(' + '.join(elems))
                + '\n)'
            ]
    if bytes:
        elems += [str(bytes)]
    return 'return {0};\n'.format(' + '.join(elems))

def generate_struct_fields(node):
    bound = {m.bound:m for m in node.members if m.bound}
    text = ''
    for m in node.members:
        if m.fixed:
            text += '{0} {1}[{2}];\n'.format(BUILTIN2C.get(m.type, m.type), m.name, m.size)
        elif m.dynamic:
            text += 'std::vector<{0}> {1};\n'.format(BUILTIN2C.get(m.type, m.type), m.name)
        elif m.limited:
            text += 'std::vector<{0}> {1}; /// limit {2}\n'.format(BUILTIN2C.get(m.type, m.type), m.name, m.size)
        elif m.greedy:
            text += 'std::vector<{0}> {1}; /// greedy\n'.format(BUILTIN2C.get(m.type, m.type), m.name)
        elif m.optional:
            text += 'bool has_{0};\n'.format(m.name)
            text += '{0} {1};\n'.format(BUILTIN2C.get(m.type, m.type), m.name)
        elif m.name in bound:
            pass
        else:
            text += '{0} {1};\n'.format(BUILTIN2C.get(m.type, m.type), m.name)
    return text

def generate_struct_constructor(node):
    def get_initializer(m):
        if isinstance(m.definition, model.Enum):
            return m.definition.members[0].name
        while isinstance(m.definition, model.Typedef):
            m = m.definition
        if m.type in BUILTIN2C:
            return ''
        return None
    def try_to_append(text, m):
        init = get_initializer(m)
        if init is not None:
            text.append('{0}({1})'.format(m.name, init))
    bound = {m.bound:m for m in node.members if m.bound}
    text = []
    for m in node.members:
        if m.fixed:
            try_to_append(text, m)
        elif m.dynamic:
            pass
        elif m.limited:
            pass
        elif m.greedy:
            pass
        elif m.optional:
            text.append('has_{0}()'.format(m.name))
            try_to_append(text, m)
        elif m.name in bound:
            pass
        else:
            try_to_append(text, m)
    return ', '.join(text)

def generate_union_decode(node):
    discpad = (node.alignment > DISC_SIZE) and (node.alignment - DISC_SIZE) or 0
    def gen_case(member):
        return ('case {0}::discriminator_{1}: if (!do_decode_in_place<E>(x.{1}, pos, end)) return false; break;\n'
            .format(node.name, member.name))
    return (
        'if (!do_decode<E>(x.discriminator, pos, end)) return false;\n'
        + (discpad and 'if (!do_decode_advance({0}, pos, end)) return false;\n'.format(discpad) or '')
        + 'switch (x.discriminator)\n'
        + '{\n'
        + ''.join('    ' + gen_case(m) for m in node.members)
        + '    ' + 'default: return false;\n'
        + '}\n'
        + 'return do_decode_advance({0}, pos, end);\n'.format(node.byte_size - DISC_SIZE - discpad)
    )

def generate_union_encode(node):
    discpad = (node.alignment > DISC_SIZE) and (node.alignment - DISC_SIZE) or 0
    def gen_case(member):
        return ('case {0}::discriminator_{1}: do_encode<E>(pos, x.{1}); break;\n'
            .format(node.name, member.name))
    return (
        'pos = do_encode<E>(pos, x.discriminator);\n'
        + (discpad and 'pos = pos + {0};\n'.format(discpad) or '')
        + 'switch (x.discriminator)\n'
        + '{\n'
        + ''.join('    ' + gen_case(m) for m in node.members)
        + '}\n'
        + 'pos = pos + {0};\n'.format(node.byte_size - DISC_SIZE - discpad)
    )

def generate_union_print(node):
    def gen_case(member):
        return ('case {0}::discriminator_{1}: do_print(out, indent, "{1}", x.{1}); break;\n'
            .format(node.name, member.name))
    return (
        'switch (x.discriminator)\n'
        + '{\n'
        + ''.join('    ' + gen_case(m) for m in node.members)
        + '}\n'
    )

def generate_union_encoded_byte_size(node):
    return str(node.byte_size)

def generate_union_get_byte_size(node):
    return 'return {0};\n'.format(node.byte_size)

def generate_union_fields(node):
    body = ',\n'.join('    discriminator_{0} = {1}'.format(m.name, m.discriminator) for m in node.members) + '\n'
    fields = ''.join('{0} {1};\n'.format(BUILTIN2C.get(m.type, m.type), m.name) for m in node.members)
    return 'enum _discriminator\n{\n' + body + '} discriminator;\n' + '\n' + fields

def generate_union_constructor(node):
    text = ['discriminator(discriminator_{0})'.format(node.members[0].name)]
    text += ['{0}()'.format(m.name) for m in node.members if m.type in BUILTIN2C]
    return ', '.join(text)

_header = """\
#ifndef _PROPHY_GENERATED_FULL_{0}_HPP
#define _PROPHY_GENERATED_FULL_{0}_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>

namespace prophy
{{
namespace generated
{{
"""

_footer = """\
}} // namespace generated
}} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_{0}_HPP */
"""

_hpp_visitor = {
    model.Include: generate_include_definition,
    model.Constant: generate_constant_definition,
    model.Typedef: generate_typedef_definition,
    model.Struct: generate_struct_definition,
    model.Enum: generate_enum_definition,
    model.Union: generate_union_definition
}

def _hpp_generator(nodes):
    last_node = None
    for node in nodes:
        prepend_newline = bool(last_node
                               and (isinstance(last_node, (model.Enum, model.Struct, model.Union))
                                    or type(last_node) is not type(node)))
        yield (prepend_newline and '\n' or '') + _hpp_visitor[type(node)](node)
        last_node = node

def generate_hpp_content(nodes):
    return ''.join(_hpp_generator(nodes))

class CppFullGenerator(object):

    def __init__(self, output_dir = "."):
        self.output_dir = output_dir

    def generate_hpp(self, nodes, basename):
        return '\n'.join((_header.format(basename), generate_hpp_content(nodes), _footer.format(basename)))
