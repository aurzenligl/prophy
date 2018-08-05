from .scalar import u32
from .data_types import base_array, build_container_length_field, distance_to_next_multiply, struct_packed
from .desc_item import descriptor_item_type, codec_kind
from .exception import ProphyError
from .six import long, string_types


class _generator_base(type):
    """
        Base metaclass type intended to validate, supplement and create all
        prophy_data_object classes.
        All of this magic happen at the very moment of the created class' import.
    """
    _slots = []

    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = cls._slots
        return super(_generator_base, cls).__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        if not hasattr(self, "_generated"):
            self._generated = True
            self._build_up_implementation()
        super(_generator_base, self).__init__(name, bases, attrs)

    def _build_up_implementation(self):
        """
            Implementation of type creation. To be overridden in derived metaclasses.
        """


class _composite_generator_base(_generator_base):

    def _build_up_implementation(self):
        self._descriptor = [descriptor_item_type(*item) for item in self._descriptor]
        self.validate()
        self.add_attributes()
        self.extend_descriptor()
        self.add_properties()
        self.add_sizers()

    def _types(self):
        for item in self._descriptor:
            yield item.type

    def add_attributes(self):
        pass

    def extend_descriptor(self):
        for raw_item in self._descriptor:
            raw_item.evaluate_codecs()

    def add_properties(self):
        pass

    def add_sizers(self):
        pass


class enum_generator(_generator_base):

    def _build_up_implementation(self):
        self.validate()
        self.add_attributes()

    def validate(self):
        for name, number in self._enumerators:
            if not isinstance(name, string_types):
                raise ProphyError("enum member's first argument has to be string")

            if not isinstance(number, (int, long)):
                raise ProphyError("enum member's second argument has to be an integer")

        names = set(name for name, _ in self._enumerators)
        if len(names) < len(self._enumerators):
            raise ProphyError("names overlap in '{}' enum".format(self.__name__))

    def add_attributes(self):
        @classmethod
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
        self._check = check


class struct_generator(_composite_generator_base):
    _slots = ["_fields"]

    def validate(self):
        for item in self._descriptor:
            if not isinstance(item.name, string_types):
                raise ProphyError("member name must be a string type")
            if not hasattr(item.type, "_is_prophy_object"):
                raise ProphyError("member type must be a prophy object, is: {!r}".format(item.type))

        types = list(self._types())
        for type_ in types[:-1]:
            if type_._UNLIMITED:
                raise ProphyError("unlimited field is not the last one")

    def add_attributes(self):
        self._BOUND = None
        self._DYNAMIC = any(type_._DYNAMIC for type_ in self._types())
        self._OPTIONAL = False
        self._PARTIAL_ALIGNMENT = None
        self._SIZE = sum((type_._OPTIONAL_SIZE if type_._OPTIONAL else type_._SIZE) for type_ in self._types())
        self._UNLIMITED = any(type_._UNLIMITED for type_ in self._types())
        if not self._descriptor:
            self._ALIGNMENT = 1
        else:
            self._ALIGNMENT = max((t._OPTIONAL_ALIGNMENT if t._OPTIONAL else t._ALIGNMENT) for t in self._types())

        alignment = 1
        for type_ in reversed(list(self._types())):
            if issubclass(type_, (base_array, bytes)) and type_._DYNAMIC:
                type_._PARTIAL_ALIGNMENT = alignment
                alignment = 1
            alignment = max(type_._ALIGNMENT, alignment)
        if not issubclass(self, struct_packed) and self._descriptor:

            def get_padded_sizes():
                types = list(self._types())
                sizes = [tp._SIZE for tp in types]
                alignments = [tp._ALIGNMENT for tp in types[1:]] + [self._ALIGNMENT]
                offset = 0

                for size, alignment in zip(sizes, alignments):
                    offset += size
                    padding = distance_to_next_multiply(offset, alignment)
                    offset += padding
                    yield padding

            self._SIZE += sum(get_padded_sizes())

    def add_properties(self):
        for item in self._descriptor:
            if codec_kind.is_array(item.type):
                self.add_repeated_property(item)
            elif codec_kind.is_composite(item.type):
                self.add_composite_property(item)
            else:
                self.add_scalar_property(item)

    def add_sizers(self):
        for item in self._descriptor:
            if codec_kind.is_array(item.type) or not codec_kind.is_struct(item.type):
                if item.type._BOUND:
                    self.substitute_len_field(item)

    def add_repeated_property(self, descriptor_item):
        def getter(self_):
            value = self_._fields.get(descriptor_item.name)
            if value is None:
                value = descriptor_item.type()
                self_._fields[descriptor_item.name] = value
            return value

        def setter(self_, new_value):
            raise ProphyError("assignment to array field not allowed")

        setattr(self, descriptor_item.name, property(getter, setter))

    def add_scalar_property(self, descriptor_item):
        if descriptor_item.type._OPTIONAL:
            def getter(self_):
                return self_._fields.get(descriptor_item.name)

            def setter(self_, new_value):
                if new_value is None:
                    self_._fields[descriptor_item.name] = None
                else:
                    self_._fields[descriptor_item.name] = descriptor_item.type._check(new_value)
        else:
            def getter(self_):
                return self_._fields.get(descriptor_item.name, descriptor_item.type._DEFAULT)

            def setter(self_, new_value):
                self_._fields[descriptor_item.name] = descriptor_item.type._check(new_value)
        setattr(self, descriptor_item.name, property(getter, setter))

    def add_composite_property(self, descriptor_item):
        if descriptor_item.type._OPTIONAL:
            def getter(self_):
                return self_._fields.get(descriptor_item.name)

            def setter(self_, new_value):
                if new_value is True:
                    self_._fields[descriptor_item.name] = descriptor_item.type()
                elif new_value is None:
                    self_._fields.pop(descriptor_item.name, None)
                else:
                    raise ProphyError("assignment to composite field not allowed")
        else:
            def getter(self_):
                value = self_._fields.get(descriptor_item.name)
                if value:
                    return value
                else:
                    return self_._fields.setdefault(descriptor_item.name, descriptor_item.type())

            def setter(self_, new_value):
                raise ProphyError("assignment to composite field not allowed")
        setattr(self, descriptor_item.name, property(getter, setter))

    def substitute_len_field(self, container_item):
        sizer_name = self.validate_and_fix_sizer_name(container_item)
        sizer_item = next(item for item in self._descriptor if item.name == sizer_name)
        bound_shift = container_item.type._BOUND_SHIFT
        self.validate_sizer_type(sizer_item, container_item)

        if sizer_item.type.__name__ == "container_len":
            sizer_item.type.add_bounded_container(container_item.name)
            self.validate_bound_shift(sizer_item.type, container_item.name, bound_shift)

        else:
            sizer_item.type = build_container_length_field(sizer_item.type, container_item.name, bound_shift)
            sizer_item.evaluate_codecs()
            delattr(self, sizer_item.name)

    def validate_and_fix_sizer_name(self, container_item):
        sizer_name = container_item.type._BOUND
        items_before_sizer = self._descriptor[:self._descriptor.index(container_item)]
        all_names = [item.name for item in self._descriptor]
        names_before = [item.name for item in items_before_sizer]

        if sizer_name not in names_before:
            if sizer_name in all_names:
                msg = "Sizing member '{}' in '{}' must be placed before '{}' container."
                raise ProphyError(msg.format(sizer_name, self.__name__, container_item.name))

            msg = "Sizing member '{}' of container '{}' not found in the object '{}'."
            msg = msg.format(sizer_name, container_item.name, self.__name__)

            """ Try to be lenient. """
            there_is_sizer_ending_with_s = (sizer_name + 's') in names_before
            there_is_sizer_without_s = sizer_name.endswith('s') and sizer_name[:-1] in names_before
            there_is_exactly_one_sizer = len([n for n in names_before if n.startswith("numOf")]) == 1
            there_is_one_bound_array = len([f for f in self._descriptor if f.type._BOUND]) == 1

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

    def validate_sizer_type(self, sizer_item, container_item):
        if sizer_item.type._OPTIONAL:
            msg = "array {}.{} must not be bound to optional field"
            raise ProphyError(msg.format(self.__name__, container_item.name))
        if not issubclass(sizer_item.type, (int, long)):
            msg = "array {}.{} must be bound to an unsigned integer"
            raise ProphyError(msg.format(self.__name__, container_item.name))

    def validate_bound_shift(self, sizer_item_type, container_name, expected_bound_shift):
        msg = "Different bound shifts are unsupported in externally sized arrays ({}.{})"
        for item in self._descriptor:
            if item.name in sizer_item_type._BOUND:
                if not item.type._BOUND_SHIFT == expected_bound_shift:
                    raise ProphyError(msg.format(self.__name__, container_name))


class union_generator(_composite_generator_base):
    _slots = ["_fields", "_discriminated"]

    def validate(self):
        for type_ in self._types():
            if type_._DYNAMIC:
                raise ProphyError("dynamic types not allowed in union")
            if type_._BOUND:
                raise ProphyError("bound array/bytes not allowed in union")
            if issubclass(type_, base_array):
                raise ProphyError("static array not implemented in union")
            if type_._OPTIONAL:
                raise ProphyError("union with optional field disallowed")

    def add_attributes(self):
        self._ALIGNMENT = max(u32._ALIGNMENT, max(type_._ALIGNMENT for type_ in self._types()))
        self._BOUND = None
        self._DYNAMIC = False
        self._OPTIONAL = False
        self._PARTIAL_ALIGNMENT = None
        natural_size = self._ALIGNMENT + max(type_._SIZE for type_ in self._types())
        self._SIZE = natural_size + distance_to_next_multiply(natural_size, self._ALIGNMENT)
        self._UNLIMITED = False
        self._discriminator_type = u32

    def add_properties(self):
        self.add_union_discriminator_property()
        for item in self._descriptor:
            if codec_kind.is_composite(item.type):
                self.add_union_composite_property(item)
            else:
                self.add_union_scalar_property(item)

    def add_union_discriminator_property(self):
        def getter(self_):
            return self_._discriminated.discriminator

        def setter(self_, discriminator_name_or_value):
            for item in self_._descriptor:
                if discriminator_name_or_value in (item.name, item.discriminator):
                    if item != self_._discriminated:
                        self_._discriminated = item
                        self_._fields = {}
                    return
            raise ProphyError("unknown discriminator: {!r}".format(discriminator_name_or_value))

        setattr(self, "discriminator", property(getter, setter))

    def add_union_composite_property(self, item):
        def getter(self_):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated.discriminator)
            value = self_._fields.get(item.name)
            if value is None:
                value = item.type()
                value = self_._fields.setdefault(item.name, value)
            return value

        def setter(self_, new_value):
            raise ProphyError("assignment to composite field not allowed")
        setattr(self, item.name, property(getter, setter))

    def add_union_scalar_property(self, item):
        def getter(self_):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated.discriminator)
            return self_._fields.get(item.name, item.type._DEFAULT)

        def setter(self_, new_value):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated.discriminator)
            new_value = item.type._check(new_value)
            self_._fields[item.name] = new_value
        setattr(self, item.name, property(getter, setter))
