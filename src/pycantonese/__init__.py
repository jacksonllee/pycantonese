from importlib.metadata import version

from pycantonese.corpus import cantomap, hkcancor, read_chat, CHAT
from pycantonese.jyutping.characters import characters_to_jyutping
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.jyutping.ipa import jyutping_to_ipa
from pycantonese.jyutping.tipa import jyutping_to_tipa
from pycantonese.jyutping.yale import jyutping_to_yale
from pycantonese.pos_tagging.tagger import pos_tag
from pycantonese.stop_words import stop_words
from pycantonese.word_segmentation import segment
from pycantonese.parsing import parse_text

__version__ = version("pycantonese")

__all__ = [
    "__version__",
    "parse_text",
    "cantomap",
    "CHAT",
    "characters_to_jyutping",
    "hkcancor",
    "jyutping_to_ipa",
    "jyutping_to_tipa",
    "jyutping_to_yale",
    "parse_jyutping",
    "pos_tag",
    "read_chat",
    "stop_words",
    "segment",
]
