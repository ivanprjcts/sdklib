try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


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


def parse_params_as_tuple_list(params, separate_list_elements=True):
    to_return = []
    for elem in params:
        if params[elem] is not None:
            if isinstance(params[elem], list) and separate_list_elements:
                for list_elem in params[elem]:
                    to_return.append((elem, list_elem))
            else:
                to_return.append((elem, params[elem]))
    return to_return


def parse_args_as_tuple_list(separate_list_elements=True, **kwargs):
    to_return = []
    for elem in kwargs:
        if kwargs[elem] is not None:
            if isinstance(kwargs[elem], list) and separate_list_elements:
                for list_elem in kwargs[elem]:
                    to_return.append((elem, list_elem))
            else:
                to_return.append((elem, kwargs[elem]))
    return to_return


def safe_add_slash(item):
    if item is not None:
        to_return = "/" + str(item)
    else:
        to_return = ""
    return to_return


def safe_add_end_slash(item):
    if item is not None:
        to_return = str(item) + "/"
    else:
        to_return = ""
    return to_return


def get_url_query_params(params):
    return "?%s" % (urlencode(params))
