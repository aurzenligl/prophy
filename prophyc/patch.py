def parse(filename):
    return [line.split() for line in open(filename)]

def patch(nodes, patches):
    for i, node in enumerate(nodes):
        patch = patches.get(node.name)
        if patch:
            nodes[i] = _apply(node, patch)

def _apply(node, patch):
    return node
