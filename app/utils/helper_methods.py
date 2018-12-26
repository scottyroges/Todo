def to_camel_case(name):
    first, *rest = name.split('_')
    return first + ''.join(word.capitalize() for word in rest)
