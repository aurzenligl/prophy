from prophyc import model
from prophyc.model import DISC_SIZE, BUILTIN_SIZES

BUILTIN2C = {
    'u8': 'uint8_t',
    'u16': 'uint16_t',
    'u32': 'uint32_t',
    'u64': 'uint64_t'
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
    if node.kind == model.Kind.FIXED:
        return 'return {0};\n'.format(node.byte_size)
    else:
        def byte_size(m):
            return BUILTIN_SIZES.get(m.type) or m.definition.byte_size
        arrays = ['{0}.size() * {1}'.format(m.name, byte_size(m)) for m in node.members if m.dynamic or m.greedy]
        if node.byte_size:
            arrays = ['{0}'.format(node.byte_size)] + arrays
        return 'return {0};\n'.format(' + '.join(arrays))

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
