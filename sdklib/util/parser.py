

def parse_params(vars):
    to_return = dict()
    for elem in vars:
        if vars[elem] is not None:
            to_return[elem] = vars[elem]
    return to_return


def parse_args(**kwargs):
    to_return = dict()
    for elem in kwargs:
        if kwargs[elem] is not None:
            to_return[elem] = kwargs[elem]
    return to_return


def safe_add_slash(item):
    if item is not None:
        to_return = "/" + str(item)
    else:
        to_return = ""
    return to_return