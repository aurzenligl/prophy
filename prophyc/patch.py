from collections import namedtuple

Action = namedtuple("Action", ["action", "params"])

def parse(filename):
    def make_item(line):
        words = line.split()
        name, action = words[:2]
        params = words[2:]
        return name, Action(action, params)
    return dict(make_item(line) for line in open(filename))

def patch(nodes, patches):
    for i, node in enumerate(nodes):
        patch = patches.get(node.name)
        if patch:
            nodes[i] = _apply(node, patch)

def _apply(node, patch):
    return node
