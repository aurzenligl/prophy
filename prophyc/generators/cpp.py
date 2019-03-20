from prophyc import model
from prophyc.generators.base import GenerateError, GeneratorBase, TranslatorBase

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


class _Padder(object):
    PADDINGS = (
        (1, 'uint8_t'),
        (2, 'uint16_t'),
        (4, 'uint32_t')
    )

    def __init__(self):
        self.index = 0

    def _gen_padding_var(self, type_):
        index = self.index
        self.index += 1
        return '%s _padding%s; /// manual padding to ensure natural alignment layout\n' % (type_, index)

    def generate_padding(self, padding):
        assert 0 < padding < 8
        return ''.join(self._gen_padding_var(type_) for val, type_ in self.PADDINGS if padding & val)


class _HppIncludesTranslator(TranslatorBase):

    def translate_include(self, include):
        return '#include "{}.pp.hpp"'.format(include.name)


STRUCT_DEF_TEMPLATE = """\
PROPHY_STRUCT({align}) {name}
{{
{blocks}}};"""

STRUCT_DEF_PART_TEMPLATE = """\
PROPHY_STRUCT({align}) part{index}
{{
{block}}} _{index};
"""

UNION_DEF_TEMPLATE = """\
PROPHY_STRUCT({align}) {name}
{{
{parts}}};"""

UNION_DEF_PART_TEMPLATE = """\
enum _discriminator
{{
{enum_fields}
}} discriminator;

{padding}union
{{
{union_fields}}};
"""


class _HppDefinitionsTranslator(TranslatorBase):
    def translate_constant(self, constant):
        return 'enum {{ {} = {} }};'.format(constant.name, _to_literal(constant.value))

    def translate_typedef(self, typedef):
        tp = primitive_types.get(typedef.type_name, typedef.type_name)
        return 'typedef {} {};'.format(tp, typedef.name)

    def translate_enum(self, enum):
        members = ',\n'.join('{} = {}'.format(member.name, _to_literal(member.value))
                             for member in enum.members)
        return 'enum {}\n{{\n{}\n}};'.format(enum.name, _indent(members, 4))

    def translate_struct(self, struct):
        def gen_member(member, padder):
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

            typename = primitive_types.get(member.type_name, member.type_name)
            if member.is_array:
                annotation = build_annotation(member)
                size = member.size or 1
                if annotation:
                    field = '{0} {1}[{2}]; /// {3}\n'.format(typename, member.name, size, annotation)
                else:
                    field = '{0} {1}[{2}];\n'.format(typename, member.name, size)
            else:
                field = '{0} {1};\n'.format(typename, member.name)
            if member.optional:
                field = 'prophy::bool_t has_{0};\n'.format(member.name) + field
            if member.padding is not None and member.padding > 0:
                field += padder.generate_padding(member.padding)
            return field

        def gen_block(members, padder):
            generated = (gen_member(member, padder) for member in members)
            return _indent(''.join(generated), 4)

        def gen_part(index, part, padder):

            generated = STRUCT_DEF_PART_TEMPLATE.format(
                index=index + 2,
                block=gen_block(part, padder),
                align=part[0].alignment
            )
            return _indent(generated, 4)

        main, parts = model.partition(struct.members)
        padder = _Padder()
        blocks = '\n'.join(
            [gen_block(main, padder)] +
            [gen_part(index, part, padder) for index, part in enumerate(parts)]
        )

        return STRUCT_DEF_TEMPLATE.format(align=struct.alignment, name=struct.name, blocks=blocks)

    def translate_union(self, union):
        def gen_disc(member):
            return 'discriminator_{0} = {1}'.format(member.name, member.discriminator)

        def gen_member(member):
            typename = primitive_types.get(member.type_name, member.type_name)
            return '{0} {1};\n'.format(typename, member.name)

        enum_fields = _indent(',\n'.join(gen_disc(mem) for mem in union.members), 4)
        union_fields = _indent(''.join(gen_member(mem) for mem in union.members), 4)
        padding = (_Padder().generate_padding(4) + '\n') if union.alignment == 8 else ''

        parts = UNION_DEF_PART_TEMPLATE.format(enum_fields=enum_fields, padding=padding, union_fields=union_fields)

        return UNION_DEF_TEMPLATE.format(align=union.alignment, name=union.name, parts=_indent(parts, 4))

    @classmethod
    def _make_lines_splitter(cls, previous_node_type, current_node_type):
        if not previous_node_type:
            return ""

        if previous_node_type != current_node_type:
            return "\n\n"

        return "\n"


ENUM_SWAP_TEMPLATE = """\
template <> inline {0}* swap<{0}>({0}* in) {{ swap(reinterpret_cast<uint32_t*>(in)); return in + 1; }}"""

STRUCT_SWAP_TEMPLATE = 'template <> {0}* swap<{0}>({0}*);'

HPP_SWAPS_BLOCK_TEMPLATE = """\
namespace prophy
{{

{content}
}} // namespace prophy
"""


class _HppSwapDeclarations(TranslatorBase):
    block_template = HPP_SWAPS_BLOCK_TEMPLATE

    def _make_lines_splitter(self, previous_node_type, _):
        return "\n" if previous_node_type else ""

    def translate_enum(self, enum):
        return ENUM_SWAP_TEMPLATE.format(enum.name)

    def translate_struct(self, struct):
        return STRUCT_SWAP_TEMPLATE.format(struct.name)

    def translate_union(self, union):
        return STRUCT_SWAP_TEMPLATE.format(union.name)


def _member_access_statement(member):
    out = '&payload->%s' % member.name
    if isinstance(member, model.StructMember) and member.is_array:
        out = out[1:]
    return out


SOURCE_TEMPLATE = """\
#include <prophy/detail/prophy.hpp>

#include "{base_name}.pp.hpp"

using namespace prophy::detail;

namespace prophy
{{

{content}
}} // namespace prophy
"""

UNION_SWAP_TEMPLATE = """\
template <>
{name}* swap<{name}>({name}* payload)
{{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {{\n{cases}\
        default: break;
    }}
    return payload + 1;
}}"""

UNION_SWAP_CASE_TEMPLATE = """\
        case {name}::discriminator_{member}: swap({access}); break;
"""

STRUCT_SWAP_PART_TEMPLATE = """\
inline {name}::part{number}* swap({name}::part{number}* payload{delimiters})
{{
{members}}}
"""

STRUCT_SWAP_MAIN_TEMPLATE = """\
template <>
{name}* swap<{name}>({name}* payload)
{{
{members}}}"""


class _CppSwapTranslator(TranslatorBase):
    block_template = SOURCE_TEMPLATE

    def translate_struct(self, struct):
        def gen_member(member, delimiters=[]):
            if member.is_array:
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

        def gen_last_member(name, last_mem, delimiters=[]):
            if last_mem.kind == model.Kind.UNLIMITED or last_mem.greedy:
                return 'return cast<{0}*>({1});\n'.format(
                    name,
                    _member_access_statement(last_mem)
                )
            elif last_mem.kind == model.Kind.DYNAMIC or last_mem.is_dynamic:
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
            return STRUCT_SWAP_MAIN_TEMPLATE.format(name=struct.name, members=_indent(members, 4))

        def gen_part(part_number, part):
            names = [mem.name for mem in part]
            delimiters = [mem.bound for mem in part if mem.bound and mem.bound not in names]
            members = ''.join(gen_member(mem, delimiters) + ';\n' for mem in part[:-1])
            members += gen_last_member('{0}::part{1}'.format(struct.name, part_number), part[-1], delimiters)
            delimiters_list = ''.join(', size_t {0}'.format(x) for x in delimiters)
            return STRUCT_SWAP_PART_TEMPLATE.format(name=struct.name, number=part_number, members=_indent(members, 4),
                                                    delimiters=delimiters_list)

        main, parts = model.partition(struct.members)
        return '\n'.join([gen_part(i + 2, part) for i, part in enumerate(parts)] +
                         [gen_main(main, parts)])

    def translate_union(self, union):
        def make_members_case():
            for member in union.members:
                access = _member_access_statement(member)
                yield UNION_SWAP_CASE_TEMPLATE.format(name=union.name, member=member.name, access=access)

        return UNION_SWAP_TEMPLATE.format(name=union.name, cases=''.join(make_members_case()))


HEADER_TEMPLATE = """\
#ifndef _PROPHY_GENERATED_{base_name}_HPP
#define _PROPHY_GENERATED_{base_name}_HPP

#include <prophy/prophy.hpp>

{content}#endif  /* _PROPHY_GENERATED_{base_name}_HPP */
"""


class _HppTranslator(TranslatorBase):
    block_template = HEADER_TEMPLATE
    prerequisite_translators = [
        _HppIncludesTranslator,
        _HppDefinitionsTranslator,
        _HppSwapDeclarations
    ]


class CppGenerator(GeneratorBase):
    top_level_translators = {
        ".pp.hpp": _HppTranslator,
        ".pp.cpp": _CppSwapTranslator
    }

    def check_nodes(self, nodes):
        for n in nodes:
            if isinstance(n, (model.Struct, model.Union)) and n.byte_size is None:
                raise GenerateError('{0} byte size unknown'.format(n.name))
