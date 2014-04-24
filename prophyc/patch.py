import model
from collections import namedtuple

Action = namedtuple("Action", ["action", "params"])

def parse(filename):
    def make_item(line):
        words = line.split()
        name, action = words[:2]
        params = words[2:]
        return name, Action(action, params)
    return dict(make_item(line) for line in open(filename) if line.strip())

def patch(nodes, patches):
    for node in nodes:
        patch = patches.get(node.name)
        if patch:
            _apply(node, patch)

def _apply(node, patch):
    action = _actions.get(patch.action)
    if not action:
        raise Exception("Unknown action: %s %s" % (node.name, patch))
    action(node, patch)

def _change_field_type(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, tp = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, _, p3, p4, p5, p6 = node.members[i]
    node.members[i] = model.StructMember(p1, tp, p3, p4, p5, p6)

def _make_field_dynamic_array(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, len_name = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    p1, p2, _, _, _, _ = node.members[i]
    node.members[i] = model.StructMember(p1, p2, True, len_name, None, None)

_actions = {'change_field_type': _change_field_type,
            'make_field_dynamic_array': _make_field_dynamic_array}
