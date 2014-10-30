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
    def indent(text):
        return '    ' + text.replace('\n', '\n    ')
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
                + indent(' + '.join(elems))
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
