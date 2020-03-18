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


def to_key_val_list(value, sort=False, insensitive=False):
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

    if sort and not insensitive:
        values = sorted(value)
    elif sort:
        values = sorted(value, key=lambda t: t[0].lower())
    else:
        values = value
    return list(values)


def to_key_val_dict(values):
    """
    Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a dict, e.g.,
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

    if isinstance(values, collections.Mapping):
        values = values.items()
    elif isinstance(values, (str, bytes, bool, int)) or \
            not all([isinstance(value, (list, tuple)) and len(value) == 2 for value in values]):
        raise ValueError('cannot encode objects that are not 2-tuples')

    dict_to_return = dict()
    for k, v in values:
        if k in dict_to_return and isinstance(dict_to_return[k], list) and isinstance(v, list):
            dict_to_return[k].extend(v)
        elif k in dict_to_return and isinstance(dict_to_return[k], list):
            dict_to_return[k].append(v)
        elif k in dict_to_return:
            dict_to_return[k] = [dict_to_return[k], v]
        else:
            dict_to_return[k] = v

    return dict_to_return


def xml_string_to_dict(xml_to_parse):
    return parse_xml(xml_to_parse)


class CaseInsensitiveDict(collections.MutableMapping):
    """
    A case-insensitive ``dict``-like object.
    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.
    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive::
        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True
    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.
    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.

    This class is a copy of `requests <https://github.com/kennethreitz/requests/blob/master/requests/structures.py>`_.
    """
    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return str(dict(self.items()))
