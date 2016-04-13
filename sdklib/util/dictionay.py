import collections


def contains_subdict(d1, d2):
    for elem in d1:
        if elem not in d2 or d1[elem] != d2[elem]:
            return False
    return True


def get_dict_from_list(l, **kwargs):
    for e in l:
        if contains_subdict(kwargs, e):
            return e


def to_key_val_list(value):
    """
    Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,
    ::
        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        ValueError: cannot encode objects that are not 2-tuples.
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')

    if isinstance(value, collections.Mapping):
        value = value.items()

    return list(value)