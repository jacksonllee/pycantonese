import pkg_resources

from pycantonese.corpus import hkcancor, read_chat
from pycantonese.jyutping.characters import characters2jyutping
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.jyutping.tipa import jyutping2tipa
from pycantonese.jyutping.yale import jyutping2yale
from pycantonese.stop_words import stop_words
from pycantonese.word_segmentation import segment


__version__ = pkg_resources.get_distribution("pycantonese").version

__all__ = [
    "__version__",
    "hkcancor",
    "read_chat",
    "parse_jyutping",
    "characters2jyutping",
    "jyutping2tipa",
    "jyutping2yale",
    "stop_words",
    "segment",
]
