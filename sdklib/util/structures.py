import collections

from sdklib.util.xmltodict import parse as parse_xml


def contains_subdict(d1, d2):
    for elem in d1:
        if elem not in d2 or d1[elem] != d2[elem]:
            return False
    return True


def get_dict_from_list(l, **kwargs):
    for e in l:
        if contains_subdict(kwargs, e):
            return e


def to_key_val_list(value, sort=False):
    """
    Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,
    ::
        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'}, sort=True)
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

    if sort:
        values = sorted(value)
    else:
        values = value
    return list(values)


def to_key_val_dict(values):
    """
    Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,
    ::
        >>> to_key_val_dict([('key', 'val')])
        {'key': 'val'}
        >>> to_key_val_dict({'key': 'val'})
        {'key': 'val'}
        >>> to_key_val_dict('string')
        ValueError: dictionary update sequence element.
    """
    if values is None:
        return {}

    if isinstance(values, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')

    if isinstance(values, collections.Mapping):
        values = values.items()

    dict_to_return = dict()
    for k, v in values:
        if k in dict_to_return and isinstance(dict_to_return[k], list):
            dict_to_return[k].append(v)
        elif k in dict_to_return:
            dict_to_return[k] = [dict_to_return[k], v]
        else:
            dict_to_return[k] = v

    return dict_to_return


def xml_string_to_dict(xml_to_parse):
    return parse_xml(xml_to_parse)
