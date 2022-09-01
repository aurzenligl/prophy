import prophy
from prophy.exception import ProphyError

import six


def _is_namedtuple(object_):
    if type(object_).__bases__ == (tuple,):
        fields = getattr(type(object_), '_fields', None)
        if isinstance(fields, tuple):
            return all(isinstance(field_name, str) for field_name in fields)


def jsonize(struct_, ordered=True):
    """
        It returns a python dict/list but it supposed to be fully json-serializable.
        If ordered it reflects fields order, i.e. gives a list of name-value pairs and a dict otherwise.
    """
    try:
        if isinstance(struct_, prophy.composite.struct):
            s = ((dsc.name, jsonize(getattr(struct_, dsc.name, None), ordered)) for dsc in struct_._descriptor)
            return list(s) if ordered else dict(s)

        elif isinstance(struct_, prophy.composite.union):
            discriminated = next(
                (dsc.name for dsc in struct_._descriptor if dsc.discriminator == struct_.discriminator), None
            )
            if discriminated is None:
                raise ProphyError("Failed to get currently discriminated union field")
            return jsonize(getattr(struct_, discriminated, None), ordered)

        elif isinstance(struct_, six.string_types):
            return struct_

        elif isinstance(struct_, dict):
            return {k: jsonize(v, ordered) for k, v in struct_.items()}

        elif _is_namedtuple(struct_):
            return {f: jsonize(getattr(struct_, f), ordered) for f in struct_._fields}

        elif getattr(struct_, '__getitem__', None):
            return [jsonize(item, ordered) for item in struct_]

        else:
            return struct_

    except Exception as e:
        raise ProphyError(e)
