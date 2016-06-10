from collections import namedtuple
from . import model

Action = namedtuple("Action", ["action", "params"])

def parse(filename):
    def make_item(line):
        words = line.split()
        name, action = words[:2]
        params = words[2:]
        return name, Action(action, params)
    patches = {}
    for name, action in (make_item(line) for line in open(filename) if line.strip()):
        patches.setdefault(name, []).append(action)
    return patches

def patch(nodes, patchdict):
    for idx, node in enumerate(nodes):
        patches = patchdict.get(node.name)
        if patches:
            nodes[idx] = _apply(node, patches)

def _apply(node, patches):
    for patch in patches:
        action = _actions.get(patch.action)
        if not action:
            raise Exception("Unknown action: %s %s" % (node.name, patch))
        node = action(node, patch)
    return node

def _type(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, tp = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    mem = node.members[i]
    mem.type_ = tp
    return node

def _insert(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can insert field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 3:
        raise Exception("Change field must have 3 params: %s %s" % (node.name, patch))
    index, name, tp = patch.params

    if not _is_int(index):
        raise Exception("Index is not a number: %s %s" % (node.name, patch))
    index = int(index)

    node.members.insert(index, model.StructMember(name, tp))
    return node

def _remove(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can remove field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 1:
        raise Exception("Remove field must have 1 param: %s %s" % (node.name, patch))
    name, = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    del node.members[i]
    return node

def _dynamic(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, len_name = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    mem = node.members[i]
    mem.array = True
    mem.bound = len_name
    mem.size = None
    mem.optional = False
    return node

def _greedy(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 1:
        raise Exception("Change field must have 1 params: %s %s" % (node.name, patch))
    name, = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    mem = node.members[i]
    mem.array = True
    mem.bound = None
    mem.size = None
    mem.optional = False
    return node

def _static(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, size = patch.params

    if not _is_int(size):
        raise Exception("Size is not a number: %s %s" % (node.name, patch))

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    node.members[i].bound = None
    node.members[i].size = None

    mem = node.members[i]
    mem.array = True
    mem.bound = None
    mem.size = size
    mem.optional = False
    return node

def _limited(node, patch):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch))

    if len(patch.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch))
    name, len_array = patch.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == len_array), (None, None))
    if not member:
        raise Exception("Array len member not found: %s %s" % (node.name, patch))

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))

    mem = node.members[i]
    mem.array = True
    mem.bound = len_array
    mem.optional = False
    return node

def _struct(node, patch):
    if not isinstance(node, model.Union):
        raise Exception("Can only change union to struct: %s" % (node.name))

    if len(patch.params):
        raise Exception("Change union to struct takes no params: %s" % (node.name))

    def to_struct_member(member):
        return model.StructMember(name = member.name, type_ = member.type_, definition = member.definition)

    return model.Struct(node.name, [to_struct_member(mem) for mem in node.members])

def _rename(node, patch):
    def rename_node(node, new_name):
        node.name = patch.params[0]
        return node

    def rename_field(node, orig_name, new_name):
        if not isinstance(node, (model.Struct, model.Union)):
            raise Exception("Can rename fields only in composites: %s %s" % (node.name, patch))
        i, member = next((x for x in enumerate(node.members) if x[1].name == orig_name), (None, None))
        if not member:
            raise Exception("Member not found: %s %s" % (node.name, patch))
        member.name = new_name
        return node

    if len(patch.params) == 1:
        return rename_node(node, patch.params[0])

    if len(patch.params) == 2:
        return rename_field(node, patch.params[0], patch.params[1])

    raise Exception("Rename must have 1 or 2 params: %s %s" % (node.name, patch))

_actions = {'type': _type,
            'insert': _insert,
            'remove': _remove,
            'greedy': _greedy,
            'static': _static,
            'limited': _limited,
            'dynamic': _dynamic,
            'struct' : _struct,
            'rename' : _rename}

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
