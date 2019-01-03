from namedlist import namedlist


def dict_to_namedtuple(name, d):
    return namedlist(name, d.keys())(*d.values())


def dict_to_obj(d):
    obj = object()
    for k, v in d:
        obj.__setattr__(k, v)
    return obj
