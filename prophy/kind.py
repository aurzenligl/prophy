class Constant(type):

    def __setattr__(self, name, value):
        raise ValueError("Cannot assign to a constant.")


class kind(type):

    __metaclass__ = Constant

    INT      = 0
    ENUM     = 1
    BYTES    = 2
    ARRAY    = 3
    STRUCT   = 4
    UNION    = 5
