from functools import wraps
from string import ascii_letters, digits
import warnings


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


def _deprecate(what, use_instead, since, remove_from):
    """Create a decorator which throws a FutureWarning.

    FutureWarning is used instead of DeprecationWarning, because Python
    does not show DeprecationWarning by default.

    Parameters
    ----------
    what : str
        What to deprecate.
    use_instead : str
        Use this instead.
    since : str
        Version "x.y.z" since which the deprecation is in effect.
    remove_from : str
        Version "x.y.z" after which the deprecated functionality is removed.

    Returns
    -------
    A decorated function that throws a FutureWarning.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"'{what}' has been deprecated since PyCantonese v{since} and "
                f"will be removed from v{remove_from}. Please use "
                f"'{use_instead}' instead.",
                FutureWarning,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
