from prophyc import model

DISC_BYTE_SIZE = 4

def generate_struct_encode(node):
    text = ''
    bound = {}
    for m in reversed(node.members):
        if m.padding:
            if m.padding < 0:
                text = 'pos = align<{0}>(pos);\n'.format(abs(m.padding)) + text
            else:
                text = 'pos = pos + {0};\n'.format(m.padding) + text
        if m.fixed:
            text = 'pos = do_encode<E>(pos, x.{0}, {1});\n'.format(m.name, m.size) + text
        elif m.dynamic:
            bound[m.bound] = m
            text = 'pos = do_encode<E>(pos, x.{0}.data(), uint32_t(x.{0}.size()));\n'.format(m.name) + text
        elif m.limited:
            bound[m.bound] = m
            text = (
                'do_encode<E>(pos, x.{0}.data(), uint32_t(std::min(x.{0}.size(), size_t({1}))));\n'.format(m.name, m.size) +
                'pos = pos + {0};\n'.format(m.byte_size) + text
            )
        elif m.greedy:
            text = 'pos = do_encode<E>(pos, x.{0}.data(), x.{0}.size());\n'.format(m.name) + text
        elif m.optional:
            discpad = (m.alignment > DISC_BYTE_SIZE) and (m.alignment - DISC_BYTE_SIZE) or 0
            discpadtext = discpad and 'pos = pos + {0};\n'.format(discpad) or ''
            text = (
                'pos = do_encode<E>(pos, x.has_{0});\n'.format(m.name)
                + discpadtext
                + 'if (x.has_{0}) do_encode<E>(pos, x.{0});\n'.format(m.name)
                + 'pos = pos + {0};\n'.format(m.byte_size - DISC_BYTE_SIZE - discpad)
                + text
            )
        elif m.name in bound:
            b = bound[m.name]
            if b.dynamic:
                text = 'pos = do_encode<E>(pos, uint32_t(x.{0}.size()));\n'.format(b.name) + text
            else:
                text = (
                    'pos = do_encode<E>(pos, uint32_t(std::min(x.{0}.size(), size_t({1}))));\n'.
                    format(b.name, b.size) + text
                )
        else:
            text = 'pos = do_encode<E>(pos, x.{0});\n'.format(m.name) + text
    return text
