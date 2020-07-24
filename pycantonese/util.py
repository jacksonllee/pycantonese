ENCODING = "utf8"


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
