import prophy
from six import string_types


def _is_namedtuple(object_):
    if type(object_).__bases__ == (tuple,):
        fields = getattr(type(object_), '_fields', None)
        if isinstance(fields, tuple):
            return all(isinstance(field_name, str) for field_name in fields)


def _try_to_get_attr(obj, name):
    try:
        return getattr(obj, name)
    except AttributeError as e:
        return str(e)


def jsonize(struct_, ordered=True):
    """
        It returns a python dict/list but it supposed to be fully json-serializable.
        If ordered it reflects fields order, i.e. gives a list of name-value pairs and a dict otherwise.
    """
    try:
        if isinstance(struct_, prophy.composite.struct):
            if ordered:
                return [(dsc.name, jsonize(getattr(struct_, dsc.name, None), ordered)) for dsc in struct_._descriptor]
            else:
                return {dsc.name: jsonize(getattr(struct_, dsc.name, None), ordered) for dsc in struct_._descriptor}

        elif isinstance(struct_, prophy.composite.union):
            discriminated = next(
                (dsc.name for dsc in struct_._descriptor if dsc.discriminator == struct_.discriminator), None
            )
            assert discriminated is not None, "Failed to get currently discriminated union field"
            return jsonize(getattr(struct_, discriminated, None), ordered)

        elif isinstance(struct_, string_types):
            return struct_

        elif isinstance(struct_, dict):
            return {k: jsonize(v, ordered) for k, v in struct_.iteritems()}

        elif _is_namedtuple(struct_):
            return {f: jsonize(getattr(struct_, f), ordered) for f in struct_._fields}

        elif getattr(struct_, '__getitem__', None):
            return [jsonize(item, ordered) for item in struct_]

        else:
            return struct_

    except Exception as e:
        error_msg = 'Failed to dictionize {}: {}: {}'.format(type(struct_).__name__, type(e).__name__, e)
        print(error_msg)
        return error_msg
