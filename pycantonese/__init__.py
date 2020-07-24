import pkg_resources

from pycantonese.corpus import hkcancor, read_chat
from pycantonese.jyutping import parse_jyutping, jyutping2tipa, jyutping2yale
from pycantonese.stop_words import stop_words


__version__ = pkg_resources.get_distribution("pycantonese").version

__all__ = [
    "__version__",
    "hkcancor",
    "read_chat",
    "parse_jyutping",
    "jyutping2tipa",
    "jyutping2yale",
    "stop_words",
]
