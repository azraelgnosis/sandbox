from __init__ import STRING_TYPES


def is_iter(obj): return hasattr(obj, '__iter__') and not isinstance(obj, STRING_TYPES)
