from itertools import ifilter, islice
import model

def get_include_deps(include):
    return []

def get_constant_deps(constant):
    return filter(lambda x: not x.isdigit(),
                  reduce(lambda x, y: x.replace(y, " "), "()+-", constant.value).split())

def get_typedef_deps(typedef):
    return [typedef.type]

def get_enum_deps(enum):
    return []

def get_struct_deps(struct):
    return [member.type for member in struct.members]

def get_union_deps(union):
    return [member.type for member in union.members]

def get_deps(node):
    return deps_visitor[type(node)](node)

deps_visitor = {model.Include: get_include_deps,
                model.Constant: get_constant_deps,
                model.Typedef: get_typedef_deps,
                model.Enum: get_enum_deps,
                model.Struct: get_struct_deps,
                model.Union: get_union_deps}

def model_sort_rotate(nodes, known, available, index):
    node = nodes[index]
    for dep in get_deps(node):
        if dep not in known and dep in available:
            found = next(ifilter(lambda x: x.name == dep, islice(nodes, index + 1, None)))
            found_index = nodes.index(found)
            nodes.insert(index, nodes.pop(found_index))
            return True
    known.add(node.name)
    return False

def model_sort(nodes):
    known = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])
    available = set(node.name for node in nodes)

    index = 0
    max_index = len(nodes)

    while index < max_index:
        if not model_sort_rotate(nodes, known, available, index):
            index = index + 1