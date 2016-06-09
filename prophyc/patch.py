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

def patch(nodes, patches):
    
    for idx in range(len(nodes)):
        actions = patches.get(nodes[idx].name, [])
        actions, toStruct = _has_struct(actions)
        if toStruct:
            nodes[idx] = _apply(nodes[idx], toStruct)
        for patch in actions:
            _apply(nodes[idx],patch)

def _apply(node, patch):
    action = _actions.get(patch.action)
    if not action:
        raise Exception("Unknown action: %s %s" % (node.name, patch))
    if patch.action == 'struct':
        struct = action(node, patch)
        return struct
    action(node, patch)

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

def _struct(node,patch):
    newMembers = []
    for member in node.members:
        newMember = model.StructMember(name = member.name, type_ = member.type_, definition = member.definition)
        newMembers.append(newMember)     
    temp = model.Struct(node.name,newMembers)
    return temp

def _rename_field(node,patch):
    i, member = next((x for x in enumerate(node.members) if x[1].name == patch.params[0]), (None, None))
    if not member:
        raise Exception("Member not found: %s %s" % (node.name, patch))
    member.name = patch.params[1]
    

def _rename_class(node,patch):

    node.name = patch.params[0]

    
    
_actions = {'type': _type,
            'insert': _insert,
            'remove': _remove,
            'greedy': _greedy,
            'static': _static,
            'limited': _limited,
            'dynamic': _dynamic,
            'struct' : _struct,
            'rename_field' : _rename_field,
            'rename_class' : _rename_class}

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def _has_struct(actions):
    hasStruct = [patch for patch in actions if patch.action == 'struct']
    if hasStruct:
        return [patch for patch in actions if patch.action != 'struct'], hasStruct[0]
    else:
        return actions, False 
