def matching_strings(*args) -> bool:
    if not _valid_strings(args):
        return False

    str1, str2 = args
    return str1.lower() == str2.lower()


def matching_floats(*args) -> bool:
    if not _valid_floats(args):
        return False

    float1, float2 = args
    return float1 == float2


def present_math_operator(operator: str) -> bool:
    return operator is not None and operator in ['>', '<', '==', '<=', '>=']


def valid_part_type(part_type: str or list) -> bool:
    valid_types = ['NEW', 'AFTERMARKET', 'USED']
    if isinstance(part_type, list):
        return all(pt in valid_types for pt in part_type)

    return part_type in valid_types


# Internal Functions


def _valid_strings(strings: tuple) -> bool:
    return all(isinstance(s, str) for s in strings)


def _valid_floats(floats: tuple) -> bool:
    return all(isinstance(f, float) for f in floats)
