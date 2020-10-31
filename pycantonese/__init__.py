import pkg_resources

from pycantonese.corpus import hkcancor, read_chat
from pycantonese.jyutping.characters import (
    characters_to_jyutping,
    characters2jyutping,
)
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.jyutping.tipa import jyutping_to_tipa, jyutping2tipa
from pycantonese.jyutping.yale import jyutping_to_yale, jyutping2yale
from pycantonese.pos_tagging.tagger import pos_tag
from pycantonese.stop_words import stop_words
from pycantonese.word_segmentation import segment


__version__ = pkg_resources.get_distribution("pycantonese").version

__all__ = [
    "__version__",
    "characters_to_jyutping",
    "characters2jyutping",
    "hkcancor",
    "jyutping_to_tipa",
    "jyutping_to_yale",
    "jyutping2tipa",
    "jyutping2yale",
    "parse_jyutping",
    "pos_tag",
    "read_chat",
    "stop_words",
    "segment",
]
