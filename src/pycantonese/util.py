from string import ascii_letters, digits

# What defines non-Cantonese-ness in lettered.json from rime-cantonese
_NOT_CANTONESE = ascii_letters + digits + "-"


def _split_chars_with_alphanum(chars):
    """
    Split Cantonese characters while respecting alphanumeric characters.

    :param chars: String of Cantonese chars, possibly with alphanumeric chars.

    :return: The split result that respects the alphanumeric characters.

    :rtype: tuple of str
    """
    if not chars:
        return tuple()
    if len(chars) == 1:
        return tuple(chars)
    result = []
    first = chars[0]
    for second in chars[1:]:
        if first[-1] in _NOT_CANTONESE and second in _NOT_CANTONESE:
            first += second
        else:
            result.append(first)
            first = second
    result.append(first)
    return tuple(result)
