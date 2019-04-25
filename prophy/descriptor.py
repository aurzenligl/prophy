from collections import namedtuple

import renew

from .exception import ProphyError
from .composite import codec_kind

FieldDescriptor = namedtuple("FieldDescriptor", "name, type, kind")
FieldDescriptor.__repr__ = lambda self: "<{}, {!r}, {!r}>".format(*self)


class DescriptorField(renew.Mold):
    _cls_namespace = "prophy.descriptor"
    _extra_slots = "encode_fcn", "decode_fcn"

    def __init__(self, name, type, discriminator=None):
        self.name = name
        self.type = type
        self.discriminator = discriminator
        # These two are set later in extend_descriptor
        # their value don't affect __eq__ & __ne__ result
        self.encode_fcn = None
        self.decode_fcn = None

    def __repr__(self):
        is_union_descriptor = self.discriminator is not None
        if is_union_descriptor:
            return "{}({!r}, {!r}, {!r})".format(type(self).__name__, self.name, self.type, self.discriminator)
        else:
            return "{}({!r}, {!r})".format(type(self).__name__, self.name, self.type)

    def evaluate_codecs(self):
        all_codecs = {
            codec_kind.OPTIONAL: (encode_optional, decode_optional),
            codec_kind.ARRAY_SIZER: (encode_array_delimiter, decode_array_delimiter),
            codec_kind.ARRAY: (encode_array, decode_array),
            codec_kind.COMPOSITE: (encode_composite, decode_composite),
            codec_kind.BYTES: (encode_bytes, decode_bytes),
            codec_kind.SCALAR: (encode_scalar, decode_scalar)
        }
        kind_ = codec_kind.classify(self.type)
        assert kind_ in all_codecs
        self.encode_fcn, self.decode_fcn = all_codecs.get(kind_)

        if kind_ == codec_kind.OPTIONAL:
            base_kind = codec_kind.classify(self.type.__bases__[0])
            opt_encode, opt_decode = all_codecs.get(base_kind)

            self.type._encode = staticmethod(opt_encode)
            self.type._decode = staticmethod(opt_decode)

    @property
    def kind(self):
        if codec_kind.is_array(self.type):
            return kind.ARRAY
        elif codec_kind.is_struct(self.type):
            return kind.STRUCT
        elif codec_kind.is_union(self.type):
            return kind.UNION
        elif codec_kind.is_bytes(self.type):
            return kind.BYTES
        elif codec_kind.is_enum(self.type):
            return kind.ENUM
        else:
            return kind.INT

    @property
    def descriptor_info(self):
        return FieldDescriptor(self.name, self.type, self.kind)


def encode_optional(parent, type_, value, endianness):
    if value is None:
        return b"\x00" * type_._OPTIONAL_SIZE
    else:
        return (type_._optional_type._encode(True, endianness).ljust(type_._OPTIONAL_ALIGNMENT, b'\x00') +
                type_._encode(parent, type_.__bases__[0], value, endianness))


def encode_array_delimiter(parent, type_, _, endianness):
    return type_._encode(type_.evaluate_size(parent), endianness)


def encode_array(_, __, value, endianness):
    return value._encode_impl(endianness)


def encode_composite(_, __, value, endianness):
    return value.encode(endianness)


def encode_bytes(_, type_, value, __):
    return type_._encode(value)


def encode_scalar(_, type_, value, endianness):
    return type_._encode(value, endianness)


def decode_optional(parent, name, type_, data, pos, endianness, len_hints):
    value, _ = type_._optional_type._decode(data, pos, endianness)
    opt_alignment = type_._OPTIONAL_ALIGNMENT
    if value:
        setattr(parent, name, True)
        sub_type = type_.__bases__[0]
        pos += opt_alignment
        return opt_alignment + type_._decode(parent, name, sub_type, data, pos, endianness, len_hints)
    else:
        setattr(parent, name, None)
        return opt_alignment + type_._SIZE


def decode_array_delimiter(_, __, type_, data, pos, endianness, len_hints):
    value, size = type_._decode(data, pos, endianness)
    if value < 0:
        raise ProphyError("Array delimiter must have positive value")
    for array_name in type_._BOUND:
        len_hints[array_name] = value
    return size


def decode_array(parent, name, _, data, pos, endianness, len_hints):
    return getattr(parent, name)._decode_impl(data, pos, endianness, len_hints.get(name))


def decode_composite(parent, name, _, data, pos, endianness, __):
    return getattr(parent, name)._decode_impl(data, pos, endianness, terminal=False)


def decode_bytes(parent, name, type_, data, pos, _, len_hints):
    value, size = type_._decode(data, pos, len_hints.get(name))
    setattr(parent, name, value)
    return size


def decode_scalar(parent, name, type_, data, pos, endianness, _):
    value, size = type_._decode(data, pos, endianness)
    setattr(parent, name, value)
    return size


class kind(type):
    INT = ('INT', 0)
    ENUM = ('ENUM', 1)
    BYTES = ('BYTES', 2)
    ARRAY = ('ARRAY', 3)
    STRUCT = ('STRUCT', 4)
    UNION = ('UNION', 5)
