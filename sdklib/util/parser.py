from sdklib.compat import urlencode


def _parse_params(params):
    to_return = dict()
    for elem in params:
        if params[elem] is not None:
            to_return[elem] = params[elem]
    return to_return


def parse_params(params):
    return _parse_params(params)


def parse_args(**kwargs):
    return _parse_params(kwargs)


def _parse_params_as_tuple_list(params, separate_list_elements):
    to_return = []
    for elem in params:
        if params[elem] is not None:
            if isinstance(params[elem], list) and separate_list_elements:
                for list_elem in params[elem]:
                    to_return.append((elem, list_elem))
            else:
                to_return.append((elem, params[elem]))
    return to_return


def parse_params_as_tuple_list(params, separate_list_elements=True):
    return _parse_params_as_tuple_list(params, separate_list_elements)


def parse_args_as_tuple_list(separate_list_elements=True, **kwargs):
    return _parse_params_as_tuple_list(kwargs, separate_list_elements)


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
