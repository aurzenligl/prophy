import collections

from .base_array import base_array
from .composite import codec_kind, distance_to_next_multiply, struct_packed
from .descriptor import DescriptorField
from .exception import ProphyError
from .scalar import u32
from .six import long


class _generator_base(type):
    """
        Base metaclass type intended to validate, supplement and create all
        prophy_data_object classes.
    """
    _slots = []

    def __new__(mcs, name, bases, attrs):
        attrs["__slots__"] = mcs._slots
        return super(_generator_base, mcs).__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "_generated"):
            cls._generated = True
            cls._build_up_implementation()
        super(_generator_base, cls).__init__(name, bases, attrs)

    def _build_up_implementation(cls):
        """
            Implementation of type creation. To be overridden in derived metaclasses.
        """
    def __eq__(cls, other):
        if not isinstance(other, cls.__class__):
            return NotImplemented

        def type_attr_eq(attr):
            if hasattr(cls_d.type, attr) and hasattr(other_d.type, attr):
                return getattr(cls_d.type, attr) == getattr(other_d.type, attr)

        if cls.__bases__ != other.__bases__:
            return False

        if len(cls._descriptor) != len(other._descriptor):
            return False

        for cls_d, other_d in zip(cls._descriptor, other._descriptor):

            if cls_d.name != other_d.name:
                return False

            if cls_d.discriminator != other_d.discriminator:
                return False

            if cls_d.type.__name__ == other_d.type.__name__ == '_array':
                cls_d_type, other_d_type = cls_d.type._TYPE, other_d.type._TYPE

                for f in ('_SIZE', '_BOUND', '_DYNAMIC', '_ALIGNMENT'):
                    if not type_attr_eq(f):
                        return False
                    if getattr(cls_d.type._TYPE, f) != getattr(other_d.type._TYPE, f):
                        return False

            elif cls_d.type.__name__ == other_d.type.__name__ == 'container_len':
                cls_d_type, other_d_type = cls_d.type.__name__, other_d.type.__name__

                if not type_attr_eq('__bases__'):
                    return False

                for f in ('_SIZE', '_BOUND', '_DYNAMIC', '_ALIGNMENT', '_TYPE'):
                    if not type_attr_eq(f):
                        return False

            elif cls_d.type.__name__ == other_d.type.__name__ == '_bytes':
                cls_d_type, other_d_type = cls_d.type.__name__, other_d.type.__name__

                if not type_attr_eq('__bases__'):
                    return False

                for f in ('_ALIGNMENT', '_BOUND', '_BOUND_SHIFT', '_DEFAULT', '_DYNAMIC', '_OPTIONAL', '_SIZE',
                          '_UNLIMITED'):
                    if not type_attr_eq(f):
                        return False

            elif getattr(cls_d.type, '_OPTIONAL', False) == getattr(other_d.type, '_OPTIONAL', False) \
                    == True:  # noqa: E712
                cls_d_type, other_d_type = cls_d.type._optional_type, other_d.type._optional_type

            else:
                cls_d_type, other_d_type = cls_d.type, other_d.type

            if cls_d_type != other_d_type:
                return False

        return True

    def __ne__(cls, other):
        are_equal = cls.__class__.__eq__(cls, other)
        if are_equal is NotImplemented:
            return NotImplemented
        return not are_equal


class _composite_generator_base(_generator_base):

    def _build_up_implementation(cls):
        cls._descriptor = [DescriptorField(*field) for field in cls._descriptor]
        cls.validate()
        cls.add_attributes()
        cls.extend_descriptor()
        cls.add_properties()
        cls.add_sizers()

    def _types(cls):
        for field in cls._descriptor:
            yield field.type

    def add_attributes(cls):
        """To be implemented in derived class."""

    def extend_descriptor(cls):
        for raw_item in cls._descriptor:
            raw_item.evaluate_codecs()

    def add_properties(cls):
        """To be implemented in derived class."""

    def add_sizers(cls):
        """To be implemented in derived class."""

    def validate(cls):
        """To be implemented in derived class."""


class enum_generator(_generator_base):

    def _build_up_implementation(cls):
        cls.validate()
        cls.add_attributes()

    def validate(cls):
        for name, number in cls._enumerators:
            if not isinstance(name, str):
                msg = "enum ({}) member's first argument has to be string, got '{}'"
                raise ProphyError(msg.format(cls.__name__, type(name).__name__))

            if not isinstance(number, (int, long)):
                msg = "enum member's ({}.{}) second argument has to be an integer, got '{}'"
                raise ProphyError(msg.format(cls.__name__, name, type(number).__name__))

        duplicates = ", ".join(_list_duplicates(name for name, _ in cls._enumerators))
        if duplicates:
            raise ProphyError("names overlap in '{}' enum, duplicates: {}".format(cls.__name__, duplicates))

    def add_attributes(self):
        def check(cls, value):
            if isinstance(value, str):
                value = name_to_int.get(value)
                if value is None:
                    raise ProphyError("unknown enumerator name in {}".format(cls.__name__))
                return cls(value)
            elif isinstance(value, (int, long)):
                if value not in int_to_name:
                    raise ProphyError("unknown enumerator {} value".format(cls.__name__))
                return cls(value)
            else:
                raise ProphyError("neither string nor int")

        name_to_int = {name: value for name, value in self._enumerators}
        int_to_name = {value: name for name, value in self._enumerators}
        list(map(self._check, (value for _, value in self._enumerators)))
        self._DEFAULT = self(self._enumerators[0][1])
        self._name_to_int = name_to_int
        self._int_to_name = int_to_name
        self._check = classmethod(check)

    def __eq__(cls, other):
        if not isinstance(other, cls.__class__):
            return NotImplemented
        return cls._enumerators == other._enumerators


class struct_generator(_composite_generator_base):
    _slots = ["_fields"]

    def validate(cls):
        for field in cls._descriptor:
            if not isinstance(field.name, str):
                msg = "struct ({}) member's name must be a string type, got: '{}'"
                raise ProphyError(msg.format(cls.__name__, type(field.name).__name__))
            if not hasattr(field.type, "_is_prophy_object"):
                msg = "struct member's ({}.{}) type must be a prophy object, is: {!r}"
                raise ProphyError(msg.format(cls.__name__, field.name, field.type))

        types = list(cls._types())
        for type_ in types[:-1]:
            if type_._UNLIMITED:
                raise ProphyError("unlimited field is not the last one")

    def add_attributes(cls):
        cls._BOUND = None
        cls._DYNAMIC = any(type_._DYNAMIC for type_ in cls._types())
        cls._OPTIONAL = False
        cls._PARTIAL_ALIGNMENT = None
        cls._SIZE = sum((type_._OPTIONAL_SIZE if type_._OPTIONAL else type_._SIZE) for type_ in cls._types())
        cls._UNLIMITED = any(type_._UNLIMITED for type_ in cls._types())
        if not cls._descriptor:
            cls._ALIGNMENT = 1
        else:
            cls._ALIGNMENT = max((t._OPTIONAL_ALIGNMENT if t._OPTIONAL else t._ALIGNMENT) for t in cls._types())

        alignment = 1
        for type_ in reversed(list(cls._types())):
            if issubclass(type_, (base_array, bytes)) and type_._DYNAMIC:
                type_._PARTIAL_ALIGNMENT = alignment
                alignment = 1
            alignment = max(type_._ALIGNMENT, alignment)
        if not issubclass(cls, struct_packed) and cls._descriptor:

            def get_padded_sizes():
                types = list(cls._types())
                sizes = [tp._SIZE for tp in types]
                alignments = [tp._ALIGNMENT for tp in types[1:]] + [cls._ALIGNMENT]
                offset = 0

                for size, alignment in zip(sizes, alignments):
                    offset += size
                    padding = distance_to_next_multiply(offset, alignment)
                    offset += padding
                    yield padding

            cls._SIZE += sum(get_padded_sizes())

    def add_properties(cls):
        for field in cls._descriptor:
            if codec_kind.is_array(field.type):
                cls.add_repeated_property(field)
            elif codec_kind.is_composite(field.type):
                cls.add_composite_property(field)
            else:
                cls.add_scalar_property(field)

    def add_sizers(cls):
        for field in cls._descriptor:
            if codec_kind.is_array(field.type) or not codec_kind.is_struct(field.type):
                if field.type._BOUND:
                    cls.substitute_len_field(field)

    def add_repeated_property(cls, descriptor_field):
        def getter(self):
            value = self._fields.get(descriptor_field.name)
            if value is None:
                value = descriptor_field.type()
                self._fields[descriptor_field.name] = value
            return value

        def setter(self, new_value):
            raise ProphyError("assignment to array field not allowed")

        setattr(cls, descriptor_field.name, property(getter, setter))

    def add_scalar_property(cls, descriptor_field):
        if descriptor_field.type._OPTIONAL:
            def getter(self):
                return self._fields.get(descriptor_field.name)

            def setter(self, new_value):
                if new_value is None:
                    self._fields[descriptor_field.name] = None
                else:
                    self._fields[descriptor_field.name] = descriptor_field.type._check(new_value)
        else:
            def getter(self):
                return self._fields.get(descriptor_field.name, descriptor_field.type._DEFAULT)

            def setter(self, new_value):
                self._fields[descriptor_field.name] = descriptor_field.type._check(new_value)
        setattr(cls, descriptor_field.name, property(getter, setter))

    def add_composite_property(cls, descriptor_field):
        if descriptor_field.type._OPTIONAL:
            def getter(self):
                return self._fields.get(descriptor_field.name)

            def setter(self, new_value):
                if new_value is True:
                    self._fields[descriptor_field.name] = descriptor_field.type()
                elif new_value is None:
                    self._fields.pop(descriptor_field.name, None)
                else:
                    raise ProphyError("assignment to composite field not allowed")
        else:
            def getter(self):
                value = self._fields.get(descriptor_field.name)
                if value:
                    return value
                else:
                    return self._fields.setdefault(descriptor_field.name, descriptor_field.type())

            def setter(self, new_value):
                raise ProphyError("assignment to composite field not allowed")
        setattr(cls, descriptor_field.name, property(getter, setter))

    def substitute_len_field(cls, container_item):
        sizer_name = cls.validate_and_fix_sizer_name(container_item)
        sizer_item = next(field for field in cls._descriptor if field.name == sizer_name)
        bound_shift = container_item.type._BOUND_SHIFT
        cls.validate_sizer_type(sizer_item, container_item)

        if sizer_item.type.__name__ == "container_len":
            sizer_item.type.add_bounded_container(container_item.name)
            cls.validate_bound_shift(sizer_item.type, container_item.name, bound_shift)

        else:
            sizer_item.type = build_container_length_field(sizer_item.type, container_item.name, bound_shift)
            sizer_item.evaluate_codecs()
            delattr(cls, sizer_item.name)

    def validate_and_fix_sizer_name(cls, container_item):
        sizer_name = container_item.type._BOUND
        items_before_sizer = cls._descriptor[:cls._descriptor.index(container_item)]
        all_names = [field.name for field in cls._descriptor]
        names_before = [field.name for field in items_before_sizer]

        if sizer_name not in names_before:
            if sizer_name in all_names:
                msg = "Sizing member '{}' in '{}' must be placed before '{}' container."
                raise ProphyError(msg.format(sizer_name, cls.__name__, container_item.name))

            msg = "Sizing member '{}' of container '{}' not found in the object '{}'."
            msg = msg.format(sizer_name, container_item.name, cls.__name__)

            """ Try to be lenient. """
            there_is_sizer_ending_with_s = (sizer_name + 's') in names_before
            there_is_sizer_without_s = sizer_name.endswith('s') and sizer_name[:-1] in names_before
            there_is_exactly_one_sizer = len([n for n in names_before if n.startswith("numOf")]) == 1
            there_is_one_bound_array = len([f for f in cls._descriptor if f.type._BOUND]) == 1

            if there_is_sizer_ending_with_s:
                sizer_name += 's'

            elif there_is_sizer_without_s:
                sizer_name = sizer_name[:-1]

            elif there_is_exactly_one_sizer and there_is_one_bound_array:
                sizer_name = next(f for f in items_before_sizer if f.name.startswith("numOf")).name
            else:
                raise ProphyError(msg)

            container_item.type._BOUND = sizer_name
            print("Warning: {}\n Picking '{}' as the missing sizer instead.\n".format(msg, sizer_name))

        return sizer_name

    def validate_sizer_type(cls, sizer_item, container_item):
        if sizer_item.type._OPTIONAL:
            msg = "array {}.{} must not be bound to optional field"
            raise ProphyError(msg.format(cls.__name__, container_item.name))
        if not issubclass(sizer_item.type, (int, long)):
            msg = "array {}.{} must be bound to an unsigned integer"
            raise ProphyError(msg.format(cls.__name__, container_item.name))

    def validate_bound_shift(cls, sizer_item_type, container_name, expected_bound_shift):
        msg = "Different bound shifts are unsupported in externally sized arrays ({}.{})"
        for field in cls._descriptor:
            if field.name in sizer_item_type._BOUND:
                if not field.type._BOUND_SHIFT == expected_bound_shift:
                    raise ProphyError(msg.format(cls.__name__, container_name))


def build_container_length_field(sizer_item_type, container_name, bound_shift):
    class container_len(sizer_item_type):
        _BOUND = [container_name]
        _TYPE = sizer_item_type

        @classmethod
        def add_bounded_container(cls, cont_name):
            cls._BOUND.append(cont_name)

        @classmethod
        def evaluate_size(cls, parent):
            sizes = set(len(getattr(parent, c_name)) for c_name in cls._BOUND)
            if len(sizes) != 1:
                msg = "Size mismatch of arrays in {}: {}"
                raise ProphyError(msg.format(parent.__class__.__name__, ", ".join(cls._BOUND)))
            return sizes.pop()

        @staticmethod
        def _encode(value, endianness):
            return sizer_item_type._encode(value + bound_shift, endianness)

        @staticmethod
        def _decode(data, pos, endianness):
            value, size = sizer_item_type._decode(data, pos, endianness)
            array_guard = 65536
            if value > array_guard:
                raise ProphyError("decoded array length over %s" % array_guard)
            value -= bound_shift
            if value < 0:
                raise ProphyError("decoded array length smaller than shift")
            return value, size

    return container_len


class union_generator(_composite_generator_base):
    _slots = ["_fields", "_discriminated"]

    def validate(cls):
        for type_ in cls._types():
            if type_._DYNAMIC:
                raise ProphyError("dynamic types not allowed in union")
            if type_._BOUND:
                raise ProphyError("bound array/bytes not allowed in union")
            if issubclass(type_, base_array):
                raise ProphyError("static array not implemented in union")
            if type_._OPTIONAL:
                raise ProphyError("union with optional field disallowed")

    def add_attributes(cls):
        cls._ALIGNMENT = max(u32._ALIGNMENT, max(type_._ALIGNMENT for type_ in cls._types()))
        cls._BOUND = None
        cls._DYNAMIC = False
        cls._OPTIONAL = False
        cls._PARTIAL_ALIGNMENT = None
        natural_size = cls._ALIGNMENT + max(type_._SIZE for type_ in cls._types())
        cls._SIZE = natural_size + distance_to_next_multiply(natural_size, cls._ALIGNMENT)
        cls._UNLIMITED = False
        cls._discriminator_type = u32

    def add_properties(cls):
        cls.add_union_discriminator_property()
        for field in cls._descriptor:
            if codec_kind.is_composite(field.type):
                cls.add_union_composite_property(field)
            else:
                cls.add_union_scalar_property(field)

    def add_union_discriminator_property(cls):
        def getter(self):
            return self._discriminated.discriminator

        def setter(self, discriminator_name_or_value):
            for field in self._descriptor:
                if discriminator_name_or_value in (field.name, field.discriminator):
                    if field != self._discriminated:
                        self._discriminated = field
                        self._fields = {}
                    return
            raise ProphyError("unknown discriminator: {!r}".format(discriminator_name_or_value))

        setattr(cls, "discriminator", property(getter, setter))

    def add_union_composite_property(cls, field):
        def getter(self):
            if self._discriminated is not field:
                raise ProphyError("currently field %s is discriminated" % self._discriminated.discriminator)
            value = self._fields.get(field.name)
            if value is None:
                value = field.type()
                value = self._fields.setdefault(field.name, value)
            return value

        def setter(self, new_value):
            raise ProphyError("assignment to composite field not allowed")

        setattr(cls, field.name, property(getter, setter))

    def add_union_scalar_property(cls, field):
        def getter(self):
            if self._discriminated is not field:
                raise ProphyError("currently field %s is discriminated" % self._discriminated.discriminator)
            return self._fields.get(field.name, field.type._DEFAULT)

        def setter(self, new_value):
            if self._discriminated is not field:
                raise ProphyError("currently field %s is discriminated" % self._discriminated.discriminator)
            new_value = field.type._check(new_value)
            self._fields[field.name] = new_value

        setattr(cls, field.name, property(getter, setter))


def _list_duplicates(iterable):
    iterable = list(iterable)
    return sorted((collections.Counter(iterable) - collections.Counter(set(iterable))).keys())
