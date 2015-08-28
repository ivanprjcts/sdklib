
def contains_subdict(d1, d2):
    for elem in d1:
        if elem not in d2 or d1[elem] != d2[elem]:
            return False
    return True


def get_dict_from_list(l, **kwargs):
    for e in l:
        if contains_subdict(kwargs, e):
            return e
