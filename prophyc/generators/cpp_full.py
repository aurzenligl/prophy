from prophyc import model
from prophyc.model import DISC_SIZE, BUILTIN_SIZES
from prophyc.generators.base import GenerateError, GeneratorBase, TranslatorBase

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


# flake8: noqa E501

def _indent(text):
    return '\n'.join(x and '    ' + x or '' for x in text.split('\n'))


def _get_initializer(m):
    while isinstance(m.definition, model.Typedef):
        m = m.definition
    if isinstance(m.definition, model.Enum):
        return m.definition.members[0].name
    if m.type_name in BUILTIN2C:
        return ''
    return None


def _const_refize(apply_, text):
    return apply_ and text.join(('const ', '&')) or text


def _get_leaf(node):
    """
    Gets innermost definition of Typedef or Struct-/UnionMember.
    Other nodes pass through.
    """
    while getattr(node, 'definition', None):
        node = node.definition
    return node


def _get_byte_size(node):
    """Gets byte size of any node."""
    node = _get_leaf(node)
    if isinstance(node, model.Enum):
        return DISC_SIZE
    elif hasattr(node, 'type_name'):
        return BUILTIN_SIZES.get(node.type_name)
    else:
        return node.byte_size


def _get_cpp_builtin_type(node):
    """Gets C++ float or int type from stdint.h, or throws miserably."""
    return BUILTIN2C[_get_leaf(node).type_name]


def _to_literal(value):
    try:
        return '{}{}'.format(value, int(value, 0) > 0 and 'u' or '')
    except ValueError:
        return value


class _HppIncludesTranslator(TranslatorBase):
    block_template = "{content}"

    def translate_include(self, include):
        return '#include "{}.ppf.hpp"'.format(include.name)


class _HppDefinitionsTranslator(TranslatorBase):
    block_template = """\
namespace prophy
{{
namespace generated
{{

{content}
}} // namespace generated
}} // namespace prophy
"""

    def translate_constant(self, constant):
        return 'enum {{ {} = {} }};'.format(constant.name, _to_literal(constant.value))

    def translate_enum(self, enum):
        body = ',\n'.join('    {0} = {1}'.format(m.name, _to_literal(m.value)) for m in enum.members) + '\n'
        return 'enum {0}\n'.format(enum.name) + '{\n' + body + '};'

    def translate_typedef(self, node):
        return 'typedef {0} {1};'.format(BUILTIN2C.get(node.type_name, node.type_name), node.name)

    def translate_struct(self, node):
        return (
                'struct {0} : public prophy::detail::message<{0}>\n'.format(node.name) +
                '{\n' +
                _indent(
                    '\n'.join((
                        'enum {{ encoded_byte_size = {0} }};\n'.format(generate_struct_encoded_byte_size(node)),
                        generate_struct_fields(node),
                        generate_struct_constructor(node),
                        'size_t get_byte_size() const\n' +
                        '{\n' +
                        _indent(generate_struct_get_byte_size(node)) +
                        '}\n'
                    ))
                ) +
                '};'
        )

    def translate_union(self, node):
        return (
                'struct {0} : public prophy::detail::message<{0}>\n'.format(node.name) +
                '{\n' +
                _indent(
                    '\n'.join((
                        'enum {{ encoded_byte_size = {0} }};\n'.format(generate_union_encoded_byte_size(node)),
                        generate_union_fields(node),
                        generate_union_constructor(node),
                        'size_t get_byte_size() const\n' +
                        '{\n' +
                        _indent(generate_union_get_byte_size(node)) +
                        '}\n'
                    ))
                ) +
                '};'
        )

    @classmethod
    def _make_lines_splitter(cls, previous_node_type, current_node_type):
        if not previous_node_type:
            return ""

        if previous_node_type in ("Enum", "Struct", "Union") or current_node_type in ("Enum", "Struct", "Union"):
            return "\n\n\n"

        if previous_node_type != current_node_type:
            return "\n\n"

        return "\n"


HPP_HEADER_TEMPLATE = """\
#ifndef _PROPHY_GENERATED_FULL_{base_name}_HPP
#define _PROPHY_GENERATED_FULL_{base_name}_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/array.hpp>
#include <prophy/endianness.hpp>
#include <prophy/optional.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>
#include <prophy/detail/mpl.hpp>

{content}
#endif  /* _PROPHY_GENERATED_FULL_{base_name}_HPP */
"""


class _HppTranslator(TranslatorBase):
    block_template = HPP_HEADER_TEMPLATE
    prerequisite_translators = [
        _HppIncludesTranslator,
        _HppDefinitionsTranslator
    ]

    @classmethod
    def _make_lines_splitter(cls, previous_node_type, current_node_type):
        if not previous_node_type:
            return ""
        if previous_node_type in ("Enum", "Struct", "Union") or current_node_type in ("Enum", "Struct", "Union"):
            return "\n\n"
        return TranslatorBase._make_lines_splitter(previous_node_type, current_node_type)


CPP_SOURCE_TEMPLATE = """\
#include "{base_name}.ppf.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/printer.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy::generated;

namespace prophy
{{
namespace detail
{{

{content}
}} // namespace detail
}} // namespace prophy
"""


class _CppTranslator(TranslatorBase):
    block_template = CPP_SOURCE_TEMPLATE

    def translate_enum(self, node):
        return (
                'template <>\n' +
                'const char* print_traits<{0}>::to_literal({0} x)\n'.format(node.name) +
                '{\n' +
                _indent(
                    'switch (x)\n' +
                    '{\n' +
                    _indent(
                        ''.join('case {0}: return "{0}";\n'.format(m.name) for m in node.members) +
                        'default: return 0;\n'
                    ) +
                    '}\n'
                ) +
                '}'
        )

    def translate_struct(self, node):
        def encode_impl(node):
            cast_template = 'template uint8_t* message_impl<{0}>::encode<{1}>(const {0}& x, uint8_t* pos);\n'
            return (
                    'template <>\n' +
                    'template <endianness E>\n' +
                    'uint8_t* message_impl<{0}>::encode(const {0}& x, uint8_t* pos)\n'.format(node.name) +
                    '{\n' +
                    _indent(
                        generate_struct_encode(node) +
                        'return pos;\n'
                    ) +
                    '}\n' +
                    ''.join(cast_template.format(node.name, e) for e in ('native', 'little', 'big'))
            )

        def decode_impl(node):
            cast_template = 'template bool message_impl<{0}>::decode<{1}>' \
                            '({0}& x, const uint8_t*& pos, const uint8_t* end);\n'
            return (
                    'template <>\n' +
                    'template <endianness E>\n' +
                    'bool message_impl<{0}>::decode({0}& x, const uint8_t*& pos, const uint8_t* end)\n'.format(
                        node.name) +
                    '{\n' +
                    _indent(
                        'return (\n' +
                        _indent(generate_struct_decode(node)) +
                        ');\n'
                    ) +
                    '}\n' + ''.join(cast_template.format(node.name, e) for e in ('native', 'little', 'big'))
            )

        def print_impl(node):
            cast_template = 'template void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent);'
            return (
                    'template <>\n' +
                    'void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent)\n'.format(
                        node.name) +
                    '{\n' +
                    _indent(generate_struct_print(node)) +
                    '}\n' + cast_template.format(node.name)
            )

        return (
                encode_impl(node) + '\n' +
                decode_impl(node) + '\n' +
                print_impl(node)
        )

    def translate_union(self, node):
        def encode_impl(node):
            return (
                    'template <>\n' +
                    'template <endianness E>\n' +
                    'uint8_t* message_impl<{0}>::encode(const {0}& x, uint8_t* pos)\n'.format(node.name) +
                    '{\n' +
                    _indent(
                        generate_union_encode(node) +
                        'return pos;\n'
                    ) +
                    '}\n' +
                    ''.join(
                        'template uint8_t* message_impl<{0}>::encode<{1}>(const {0}& x, uint8_t* pos);\n'.format(
                            node.name, e)
                        for e in ('native', 'little', 'big')
                    )
            )

        def decode_impl(node):
            return (
                    'template <>\n' +
                    'template <endianness E>\n' +
                    'bool message_impl<{0}>::decode({0}& x, const uint8_t*& pos, const uint8_t* end)\n'.format(
                        node.name) +
                    '{\n' +
                    _indent(generate_union_decode(node)) +
                    '}\n' +
                    ''.join(
                        'template bool message_impl<{0}>::decode<{1}>({0}& x, const uint8_t*& pos, const uint8_t* end);\n'.format(
                            node.name, e)
                        for e in ('native', 'little', 'big')
                    )
            )

        def print_impl(node):
            return (
                    'template <>\n' +
                    'void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent)\n'.format(
                        node.name) +
                    '{\n' +
                    _indent(generate_union_print(node)) +
                    '}\n' +
                    'template void message_impl<{0}>::print(const {0}& x, std::ostream& out, size_t indent);\n'.format(
                        node.name)
            )

        return (
                encode_impl(node) + '\n' +
                decode_impl(node) + '\n' +
                print_impl(node)
        )


def generate_struct_encode(node):
    text = ''
    bound = {m.bound: m for m in node.members if m.bound}
    delimiters = {bound[m.name].name: (m, _get_cpp_builtin_type(m)) for m in node.members if m.name in bound}

    for m in node.members:
        if m.is_fixed:
            text += 'pos = do_encode<E>(pos, x.{0}.data(), {1});\n'.format(m.name, m.size)
        elif m.is_dynamic:
            d, dcpptype = delimiters[m.name]
            text += 'pos = do_encode<E>(pos, x.{0}.data(), {1}(x.{0}.size()));\n'.format(m.name, dcpptype)
        elif m.is_limited:
            d, dcpptype = delimiters[m.name]
            dcpptype = _get_cpp_builtin_type(d)
            text += ('do_encode<E>(pos, x.{0}.data(), {2}(std::min(x.{0}.size(), size_t({1}))));\n'
                     'pos = pos + {3};\n').format(m.name, m.size, dcpptype, m.byte_size)

        elif m.greedy:
            text += 'pos = do_encode<E>(pos, x.{0}.data(), x.{0}.size());\n'.format(m.name)
        elif m.optional:
            text += 'pos = do_encode<E>(pos, x.{0});\n'.format(m.name)
        elif m.name in bound:
            b = bound[m.name]
            mcpptype = _get_cpp_builtin_type(m)
            if b.is_dynamic:
                text += 'pos = do_encode<E>(pos, {1}(x.{0}.size()));\n'.format(b.name, mcpptype)
            else:
                text += (
                    'pos = do_encode<E>(pos, {2}(std::min(x.{0}.size(), size_t({1}))));\n'
                        .format(b.name, b.size, mcpptype)
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
    bound = {m.bound: m for m in node.members if m.bound}
    for m in node.members:
        if m.is_fixed:
            text.append('do_decode<E>(x.{0}.data(), {1}, pos, end)'.format(m.name, m.size))
        elif m.is_dynamic:
            text.append('do_decode<E>(x.{0}.data(), x.{0}.size(), pos, end)'.format(m.name))
        elif m.is_limited:
            text.append('do_decode_in_place<E>(x.{0}.data(), x.{0}.size(), pos, end)'.format(m.name))
            text.append('do_decode_advance({0}, pos, end)'.format(m.byte_size))
        elif m.greedy:
            text.append('do_decode_greedy<E>(x.{0}, pos, end)'.format(m.name))
        elif m.optional:
            text.append('do_decode<E>(x.{0}, pos, end)'.format(m.name))
        elif m.name in bound:
            b = bound[m.name]
            mcpptype = _get_cpp_builtin_type(m)
            if b.is_dynamic:
                text.append('do_decode_resize<E, {1}>(x.{0}, pos, end)'.format(b.name, mcpptype))
            else:
                text.append('do_decode_resize<E, {2}>(x.{0}, pos, end, {1})'.format(b.name, b.size, mcpptype))
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
    bound = {m.bound: m for m in node.members if m.bound}
    for m in node.members:
        if m.is_array:
            if m.is_fixed:
                inner = 'x.{0}.data(), size_t({1})'.format(m.name, m.size)
            elif m.is_dynamic:
                inner = 'x.{0}.data(), x.{0}.size()'.format(m.name)
            elif m.is_limited:
                inner = 'x.{0}.data(), std::min(x.{0}.size(), size_t({1}))'.format(m.name, m.size)
            elif m.greedy:
                inner = 'x.{0}.data(), x.{0}.size()'.format(m.name)
            if m.type_name == 'byte':
                inner = inner.join(('std::make_pair(', ')'))
            text += 'do_print(out, indent, "{0}", {1});\n'.format(m.name, inner)
        elif m.optional:
            text += 'if (x.{0}) do_print(out, indent, "{0}", *x.{0});\n'.format(m.name)
        elif m.name in bound:
            pass
        else:
            text += 'do_print(out, indent, "{0}", x.{0});\n'.format(m.name)
    return text


def generate_struct_encoded_byte_size(node):
    return (node.kind == model.Kind.FIXED) and str(node.byte_size) or '-1'


def generate_struct_get_byte_size(node):
    bytes_ = 0
    elems = []
    for m in node.members:
        if m.kind == model.Kind.FIXED:
            if m.is_dynamic or m.greedy:
                elems += ['{0}.size() * {1}'.format(m.name, _get_byte_size(m))]
            else:
                bytes_ += m.byte_size + m.padding
        else:
            if m.is_dynamic or m.greedy:
                elems += [
                    'std::accumulate({0}.begin(), {0}.end(), size_t(), prophy::detail::byte_size())'.format(m.name)
                ]
            else:
                elems += ['{0}.get_byte_size()'.format(m.name)]
        if m.padding < 0:
            if bytes_:
                elems += [str(bytes_)]
                bytes_ = 0
            elems = [
                'prophy::detail::nearest<{0}>(\n'.format(abs(m.padding)) +
                _indent(' + '.join(elems)) +
                '\n)'
            ]
    if bytes_:
        elems += [str(bytes_)]
    return 'return {0};\n'.format(' + '.join(elems))


def generate_struct_fields(node):
    bound = {m.bound: m for m in node.members if m.bound}
    text = ''
    for m in node.members:
        if m.is_fixed:
            text += 'array<{0}, {1}> {2};\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.size, m.name)
        elif m.is_dynamic:
            text += 'std::vector<{0}> {1};\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.name)
        elif m.is_limited:
            text += 'std::vector<{0}> {1}; /// limit {2}\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.name,
                                                                   m.size)
        elif m.greedy:
            text += 'std::vector<{0}> {1}; /// greedy\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.name)
        elif m.optional:
            text += 'optional<{0}> {1};\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.name)
        elif m.name in bound:
            pass
        else:
            text += '{0} {1};\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.name)
    return text


def generate_struct_constructor(node):
    def add_to_default(lst, m, init):
        if init is not None:
            lst.append('{0}({1})'.format(m.name, init))

    def add_to_full(lst, const_ref, m, fmt='{0}'):
        lst.append((const_ref, fmt.format(BUILTIN2C.get(m.type_name, m.type_name)), m.name))

    bound = {m.bound: m for m in node.members if m.bound}
    default_ctor = []
    full_ctor = []
    for m in node.members:
        init = _get_initializer(m)
        if m.is_fixed:
            add_to_default(default_ctor, m, '')
            add_to_full(full_ctor, True, m, 'array<{0}, %s>' % m.size)
        elif m.is_dynamic:
            add_to_full(full_ctor, True, m, 'std::vector<{0}>')
        elif m.is_limited:
            add_to_full(full_ctor, True, m, 'std::vector<{0}>')
        elif m.greedy:
            add_to_full(full_ctor, True, m, 'std::vector<{0}>')
        elif m.optional:
            add_to_full(full_ctor, True, m, 'optional<{0}>')
        elif m.name in bound:
            pass
        else:
            add_to_default(default_ctor, m, init)
            add_to_full(full_ctor, init is None, m)
    return (
            (default_ctor and
             '{0}(): {1} {{ }}\n'.format(node.name, ', '.join(default_ctor)) or
             '{0}() {{ }}\n'.format(node.name)) +
            '{0}({1}): {2} {{ }}\n'.format(
                node.name,
                ', '.join(_const_refize(const_ref, tp) + ' _%s' %
                          idx for idx, (const_ref, tp, _) in enumerate(full_ctor, 1)),
                ', '.join('{0}(_{1})'.format(name, idx) for idx, (_, _, name) in enumerate(full_ctor, 1))
            )
    )


def generate_union_decode(node):
    discpad = (node.alignment > DISC_SIZE) and (node.alignment - DISC_SIZE) or 0

    def gen_case(member):
        return ('case {0}::discriminator_{1}: if (!do_decode_in_place<E>(x.{1}, pos, end)) return false; break;\n'
                .format(node.name, member.name))

    return (
            'if (!do_decode<E>(x.discriminator, pos, end)) return false;\n' +
            (discpad and 'if (!do_decode_advance({0}, pos, end)) return false;\n'.format(discpad) or '') +
            'switch (x.discriminator)\n' +
            '{\n' +
            ''.join('    ' + gen_case(m) for m in node.members) +
            '    ' + 'default: return false;\n' +
            '}\n' +
            'return do_decode_advance({0}, pos, end);\n'.format(node.byte_size - DISC_SIZE - discpad)
    )


def generate_union_encode(node):
    discpad = (node.alignment > DISC_SIZE) and (node.alignment - DISC_SIZE) or 0

    def gen_case(member):
        return ('case {0}::discriminator_{1}: do_encode<E>(pos, x.{1}); break;\n'
                .format(node.name, member.name))

    return (
            'pos = do_encode<E>(pos, x.discriminator);\n' +
            (discpad and 'pos = pos + {0};\n'.format(discpad) or '') +
            'switch (x.discriminator)\n' +
            '{\n' +
            ''.join('    ' + gen_case(m) for m in node.members) +
            '}\n' +
            'pos = pos + {0};\n'.format(node.byte_size - DISC_SIZE - discpad)
    )


def generate_union_print(node):
    def gen_case(member):
        return ('case {0}::discriminator_{1}: do_print(out, indent, "{1}", x.{1}); break;\n'
                .format(node.name, member.name))

    return (
            'switch (x.discriminator)\n' +
            '{\n' +
            ''.join('    ' + gen_case(m) for m in node.members) +
            '}\n'
    )


def generate_union_encoded_byte_size(node):
    return str(node.byte_size)


def generate_union_get_byte_size(node):
    return 'return {0};\n'.format(node.byte_size)


def generate_union_fields(node):
    body = ',\n'.join('discriminator_{0} = {1}'.format(m.name, m.discriminator) for m in node.members) + '\n'
    disc_defs = ''.join(
        'static const prophy::detail::int2type<discriminator_{0}> discriminator_{0}_t;\n'.format(m.name)
        for m in node.members
    )
    fields = ''.join('{0} {1};\n'.format(BUILTIN2C.get(m.type_name, m.type_name), m.name) for m in node.members)
    return 'enum _discriminator\n{\n' + _indent(body) + '} discriminator;\n' + '\n' + disc_defs + '\n' + fields


def generate_union_constructor(node):
    inits = [_get_initializer(m) for m in node.members]
    return (
            '{0}(): {1} {{ }}\n'.format(node.name, ', '.join(
                ['discriminator(discriminator_{0})'.format(node.members[0].name)] +
                ['{0}({1})'.format(m.name, init) for m, init in zip(node.members, inits) if init is not None]
            )) +
            ''.join(
                '{0}(prophy::detail::int2type<discriminator_{1}>, {2} _1): discriminator(discriminator_{1}), {1}(_1) {{ }}\n'
                    .format(node.name, m.name, _const_refize(init is None, BUILTIN2C.get(m.type_name, m.type_name)))
                for m, init in zip(node.members, inits)
            )
    )


class CppFullGenerator(GeneratorBase):
    top_level_translators = {
        ".ppf.hpp": _HppTranslator,
        ".ppf.cpp": _CppTranslator
    }

    def check_nodes(self, nodes):
        for n in nodes:
            if isinstance(n, (model.Struct, model.Union)) and n.byte_size is None:
                raise GenerateError('{0} byte size unknown'.format(n.name))
            if isinstance(n, model.Struct):
                occured = set()
                for m in n.members:
                    if m.bound:
                        if m.bound in occured:
                            raise GenerateError('Multiple arrays bounded by the same member ({}) in struct {} is '
                                                'not supported'.format(m.bound, n.name))
                        else:
                            occured.add(m.bound)
