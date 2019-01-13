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
        return [field.descriptor_info for field in cls._descriptor]
