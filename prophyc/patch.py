import codecs
from collections import namedtuple, defaultdict

from . import model

Action = namedtuple("Action", ["action", "params"])


def parse(filename):
    patches = defaultdict(list)
    with codecs.open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip():
                words = line.split()
                name, action = words[:2]
                params = words[2:]
                patches[name].append(Action(action, params))
    return dict(patches)


def patch(nodes, patch_dict):
    for idx, node in enumerate(nodes):
        patches = patch_dict.get(node.name)
        if patches:
            nodes[idx] = _apply(node, patches)


def _apply(node, patches):
    for patch_ in patches:
        action = _actions.get(patch_.action)
        if not action:
            raise Exception("Unknown action: %s %s" % (node.name, patch_))
        node = action(node, patch_)
    return node


def _type(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch_))
    name, tp = patch_.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch_))

    mem = node.members[i]
    mem.type_name = tp
    return node


def _insert(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can insert field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 3:
        raise Exception("Change field must have 3 params: %s %s" % (node.name, patch_))
    index, name, tp = patch_.params

    if not _is_int(index):
        raise Exception("Index is not a number: %s %s" % (node.name, patch_))
    index = int(index)

    node.members.insert(index, model.StructMember(name, tp))
    return node


def _remove(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can remove field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 1:
        raise Exception("Remove field must have 1 param: %s %s" % (node.name, patch_))
    name, = patch_.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch_))

    del node.members[i]
    return node


def _dynamic(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch_))
    name, len_name = patch_.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch_))

    mem = node.members[i]
    mem.bound = len_name
    mem.size = None
    mem.optional = False
    return node


def _greedy(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 1:
        raise Exception("Change field must have 1 params: %s %s" % (node.name, patch_))
    name, = patch_.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch_))

    mem = node.members[i]
    mem.greedy = True
    mem.bound = None
    mem.size = None
    mem.optional = False
    return node


def _static(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch_))
    name, size = patch_.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch_))

    node.members[i].bound = None
    node.members[i].size = None

    mem = node.members[i]
    mem.bound = None
    mem.size = size
    mem.optional = False
    return node


def _limited(node, patch_):
    if not isinstance(node, model.Struct):
        raise Exception("Can change field only in struct: %s %s" % (node.name, patch_))

    if len(patch_.params) != 2:
        raise Exception("Change field must have 2 params: %s %s" % (node.name, patch_))
    name, len_array = patch_.params

    i, member = next((x for x in enumerate(node.members) if x[1].name == name), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch_))

    sizer_found = len(tuple(x for x in node.members[:i] if x.name == len_array))
    if not sizer_found:
        raise Exception("Array len member not found: %s %s" % (node.name, patch_))

    mem = node.members[i]
    mem.bound = len_array
    mem.optional = False
    return node


def _struct(node, patch_):
    if not isinstance(node, model.Union):
        raise Exception("Can only change union to struct: %s" % node.name)

    if len(patch_.params):
        raise Exception("Change union to struct takes no params: %s" % node.name)

    def to_struct_member(member):
        return model.StructMember(name=member.name, type_name=member.type_name, definition=member.definition)

    return model.Struct(node.name, [to_struct_member(mem) for mem in node.members])


def _rename(node, patch_):
    def rename_node(node_, new_name):
        node_.name = new_name
        return node_

    def rename_field(node_, orig_name, new_name):
        if not isinstance(node_, (model.Struct, model.Union)):
            raise Exception("Can rename fields only in composites: %s %s" % (node_.name, patch_))
        member = next((x for x in node_.members if x.name == orig_name), None)
        if not member:
            raise Exception("Member not found: %s %s" % (node_.name, patch_))
        member.name = new_name
        return node_

    if len(patch_.params) == 1:
        return rename_node(node, patch_.params[0])

    if len(patch_.params) == 2:
        return rename_field(node, patch_.params[0], patch_.params[1])

    raise Exception("Rename must have 1 or 2 params: %s %s" % (node.name, patch_))


_actions = {
    'type': _type,
    'insert': _insert,
    'remove': _remove,
    'greedy': _greedy,
    'static': _static,
    'limited': _limited,
    'dynamic': _dynamic,
    'struct': _struct,
    'rename': _rename
}


def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
