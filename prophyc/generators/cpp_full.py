from prophyc import model

def generate_struct_encode(node):
    text = ''
    for m in node.members:
        text += 'pos = do_encode<E>(pos, x.{});\n'.format(m.name)
    return text
