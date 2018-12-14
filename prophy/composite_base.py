from .exception import ProphyError
from .scalar import prophy_data_object


class _composite_base(prophy_data_object):
    __slots__ = []

    def copy_from(self, other):
        self.validate_copy_from(other)
        if other is self:
            return

        self._fields.clear()
        self._copy_implementation(other)

    @classmethod
    def validate_copy_from(cls, rhs):
        if not isinstance(rhs, cls):
            raise TypeError("Parameter to copy_from must be instance of same class.")

    def _copy_implementation(self, other):
        " To be overrided in derived class "

    @classmethod
    def get_descriptor(cls):
        """
            FIXME: I'm afraid it rapes YAGNI rule
        """
        return [field.descriptor_info for field in cls._descriptor]

    @classmethod
    def _bricks_walk(cls, cursor):
        def eval_path(leaf_path):
            return ".%s%s" % (field.name, leaf_path or "")

        for field in cls._descriptor:

            padding_size = cursor.distance_to_next(field.type._ALIGNMENT)
            if padding_size:
                yield make_padding(padding_size), eval_path(".:pre_padding")

            for sub_brick_type, sub_brick_path in field.type._bricks_walk(cursor):
                yield sub_brick_type, eval_path(sub_brick_path)

            if field.type._PARTIAL_ALIGNMENT:
                padding_size = cursor.distance_to_next(field.type._PARTIAL_ALIGNMENT)
                if padding_size:
                    yield make_padding(padding_size), eval_path(".:partial_padding")

        padding_size = cursor.distance_to_next(cls._ALIGNMENT)
        if padding_size:
            yield make_padding(padding_size), eval_path(".:final_padding")

    @classmethod
    def wire_pattern(cls):
        cursor = _cursor_class()
        for type_, path_ in cls._bricks_walk(cursor):
            type_size = getattr(type_, "_SIZE", "??")
            if type_size != "??":
                cursor.pos += type_size
            yield path_, type_.__name__, type_size


class _cursor_class(object):
    """
        A helper for breaking variables scope while passing the "self.pos" between _bricks_walk iterators call.
        TODO: It will be probably not needed.
    """

    def __init__(self):
        self.pos = 0

    def distance_to_next(self, alignment):
        remainer = self.pos % alignment
        return (alignment - remainer) % alignment


def make_padding(padding_size):
    class PaddingMock(object):
        _SIZE = padding_size

        @staticmethod
        def encode_mock():
            return b'\x00' * padding_size

        @staticmethod
        def decode_mock(data, pos):
            if (len(data) - pos) < padding_size:
                raise ProphyError("too few bytes to decode padding")
            return data[pos:(pos + padding_size)], padding_size
    PaddingMock.__name__ = "<Pd{}>".format(padding_size)
    return PaddingMock
