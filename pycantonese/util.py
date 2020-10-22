from string import ascii_letters, digits

ENCODING = "utf8"

# What defines non-Cantonese-ness in lettered.json from rime-cantonese
_NOT_CANTONESE = ascii_letters + digits + "-"


class ListFromIterables(list):
    """
    A class like ``list`` that can be initialized with iterables.
    """

    def __init__(self, *iterables):
        super(ListFromIterables, self).__init__()
        self.input_iterables = iterables
        self.from_iterables()

    def from_iterables(self):
        for it in self.input_iterables:
            for element in it:
                self.append(element)


def get_jyutping_from_mor(mor):
    """
    Extract jyutping string from *mor*.
    """
    jyutping, _, _ = mor.partition("=")
    jyutping, _, _ = jyutping.partition("-")
    jyutping, _, _ = jyutping.partition("&")
    return jyutping


def startswithoneof(inputstr, seq):
    """
    Check if *inputstr* starts with one of the items in seq. If it does, return
        the item that it starts with. If it doe not, return ``None``.

    :param inputstr: input string

    :param seq: sequences of items to check

    :return: the item the the input string starts with (``None`` if not found)

    :rtype: str or None
    """
    seq = set(seq)
    for item in seq:
        if inputstr.startswith(item):
            return item
    else:
        return None


def endswithoneof(inputstr, seq):
    """
    Check if *inputstr* ends with one of the items in seq. If it does, return
        the item that it ends with. If it doe not, return ``None``.

    :param inputstr: input string

    :param seq: sequences of items to check

    :return: the item the the input string ends with (``None`` if not found)

    :rtype: str or None
    """
    seq = set(seq)
    for item in seq:
        if inputstr.endswith(item):
            return item
    else:
        return None


def split_characters_with_alphanum(chars):
    """
    Split Cantonese characters while respecting .

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
