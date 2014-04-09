from collections import namedtuple

Include = namedtuple("Include", ["name"])

Constant = namedtuple("Constant", ["name", "value"])

Typedef = namedtuple("Typedef", ["name", "type"])

Enum = namedtuple("Enum", ["name", "members"])
EnumMember = namedtuple("EnumMember", ["name", "value"])

Struct = namedtuple("Struct", ["name", "members"])
StructMember = namedtuple("StructMember", ["name", "type", "array", "array_bound", "array_size", "optional"])

Union = namedtuple("Union", ["name", "members"])
UnionMember = namedtuple("UnionMember", ["name", "type", "discriminator"])
