import dataclasses
import functools
import os
from typing import List, Optional, Union

from pylangacq.chat import Reader, _params_in_docstring
from pylangacq.chat import read_chat as pylangacq_read_chat
from pylangacq.objects import Gra

from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.search import _perform_search
from pycantonese.util import _deprecate


_ENCODING = "utf-8"


@dataclasses.dataclass
class Token:
    """Token with attributes as parsed from a CHAT utterance.

    Attributes
    ----------
    word : str
        Word form of the token
    pos : str
        Part-of-speech tag
    jyutping : str
        Jyutping romanization
    mor : str
        Morphological information
    gra : Gra
        Grammatical relation
    """

    __slots__ = ("word", "pos", "jyutping", "mor", "gra")

    word: str
    pos: Optional[str]
    jyutping: Optional[str]
    mor: Optional[str]
    gra: Optional[Gra]


class CHATReader(Reader):
    """A reader for Cantonese CHAT corpus files.

    .. note:: Some of the methods are inherited from the parent class
        :class:`~pylangacq.Reader` for language acquisition,
        which may or may not be applicable to your use case.
    """

    def ipsyn(self):
        """(Not implemented - the upstream ``ipsyn`` method works for English only.)"""
        raise NotImplementedError(
            "The upstream `ipsyn` method works for English only. "
            "There isn't yet a Cantonese version of IPSyn."
        )

    @staticmethod
    def _preprocess_token(t) -> Token:
        # Examples from the CHILDES LeeWongLeung corpus, child mhz
        # e.g., mor is suk1&DIM=uncle, word is 叔叔
        # e.g., mor is ngo5-PL=I, word i 我

        try:
            jyutping_mor, _, eng = t.mor.partition("=")
        except AttributeError:
            return Token(t.word, t.pos, None, t.mor, t.gra)

        if "-" in jyutping_mor:
            jyutping, _, mor = jyutping_mor.partition("-")
        elif "&" in jyutping_mor:
            jyutping, _, mor = jyutping_mor.partition("&")
        else:
            jyutping = jyutping_mor
            mor = ""

        mor = f"{mor}={eng}" if eng else mor

        try:
            parse_jyutping(jyutping)
        except ValueError:
            jyutping = None

        return Token(t.word, t.pos, jyutping or None, mor or None, t.gra)

    @_params_in_docstring("participants", "exclude", "by_utterances", "by_files")
    def jyutping(
        self, participants=None, exclude=None, by_utterances=False, by_files=False
    ) -> Union[List[str], List[List[str]], List[List[List[str]]]]:
        """Return the data in Jyutping romanization.

        Parameters
        ----------

        Returns
        -------
        List[List[List[str]]] if both by_utterances and by_files are True
        List[List[str]] if by_utterances is True and by_files is False
        List[List[str]] if by_utterances is False and by_files is True
        List[str] if both by_utterances and by_files are False
        """
        tagged_sents = self.tokens(
            participants=participants,
            exclude=exclude,
            by_utterances=True,
            by_files=True,
        )
        result = [
            [
                [tagged_word.jyutping for tagged_word in tagged_sent]
                for tagged_sent in tagged_sents_for_file
            ]
            for tagged_sents_for_file in tagged_sents
        ]
        if by_files and by_utterances:
            pass
        elif by_files and not by_utterances:
            result = [self._flatten(list, f) for f in result]
        elif not by_files and by_utterances:
            result = self._flatten(list, result)
        else:
            # not by_files and not by_utterances
            result = self._flatten(list, (self._flatten(list, f) for f in result))
        return result

    def jyutping_sents(self, participants=None, exclude=None, by_files=False):
        _deprecate(
            "jyutping_sents", "jyutping with by_utterances=True", "3.2.0", "4.0.0"
        )
        return self.jyutping(
            participants=participants,
            exclude=exclude,
            by_utterances=True,
            by_files=by_files,
        )

    def jyutpings(
        self, participants=None, exclude=None, by_utterances=False, by_files=False
    ):
        _deprecate("jyutpings", "jyutping", "3.2.0", "4.0.0")
        return self.jyutping(
            participants=participants,
            exclude=exclude,
            by_utterances=by_utterances,
            by_files=by_files,
        )

    @staticmethod
    def _get_chars_from_sent(sent: List[str]) -> List[str]:
        result = []
        for word in sent:
            if word and "\u4e00" <= word[0] <= "\u9fff":
                result.extend(list(word))
            else:
                result.append(word)
        return result

    @_params_in_docstring("participants", "exclude", "by_utterances", "by_files")
    def characters(
        self, participants=None, exclude=None, by_utterances=False, by_files=False
    ) -> Union[List[str], List[List[str]], List[List[List[str]]]]:
        """Return the data in individual Chinese characters.

        Parameters
        ----------

        Returns
        -------
        List[List[List[str]]] if both by_utterances and by_files are True
        List[List[str]] if by_utterances is True and by_files is False
        List[List[str]] if by_utterances is False and by_files is True
        List[str] if both by_utterances and by_files are False
        """
        sents = self.words(
            participants=participants,
            exclude=exclude,
            by_utterances=True,
            by_files=True,
        )
        result = [
            [self._get_chars_from_sent(sent) for sent in sents_for_file]
            for sents_for_file in sents
        ]
        if by_files and by_utterances:
            pass
        elif by_files and not by_utterances:
            result = [self._flatten(list, f) for f in result]
        elif not by_files and by_utterances:
            result = self._flatten(list, result)
        else:
            # not by_files and not by_utterances
            result = self._flatten(list, (self._flatten(list, f) for f in result))
        return result

    def character_sents(self, participants=None, exclude=None, by_files=False):
        _deprecate(
            "character_sents", "characters with by_utterances=True", "3.2.0", "4.0.0"
        )
        return self.characters(
            participants=participants,
            exclude=exclude,
            by_utterances=True,
            by_files=by_files,
        )

    def search(
        self,
        *,
        onset=None,
        nucleus=None,
        coda=None,
        tone=None,
        initial=None,
        final=None,
        jyutping=None,
        character=None,
        pos=None,
        word_range=(0, 0),
        utterance_range=(0, 0),
        sent_range=(0, 0),  # Deprecated
        by_tokens=True,
        by_utterances=False,
        tagged=None,  # Deprecated
        sents=None,  # Deprecated
        participants=None,
        exclude=None,
        by_files=False,
    ):
        """Search the data for the given criteria.

        For examples, please see https://pycantonese.org/searches.html.

        Parameters
        ----------
        onset : str, optional
            Onset to search for. A regex is supported.
        nucleus : str, optional
            Nucleus to search for. A regex is supported.
        coda : str, optional
            Coda to search for. A regex is supported.
        tone : str, optional
            Tone to search for. A regex is supported.
        initial : str, optional
            Initial to search for. A regex is supported.
            An initial, a term more prevalent in traditional Chinese
            phonology, is the equivalent of an onset.
        final : str, optional
            Final to search for.
            A final, a term more prevalent in traditional Chinese
            phonology, is the equivalent of a nucleus plus a coda.
        jyutping : str, optional
            Jyutping romanization of one Cantonese character to search for.
            If the romanization contains more than one character, a ValueError
            is raised.
        character : str, optional
            One or more Cantonese characters (within a segmented word) to
            search for.
        pos : str, optional
            A part-of-speech tag to search for. A regex is supported.
        word_range : tuple[int, int], optional
            Span of words to the left and right of a matching word to include
            in the output. The default is `(0, 0)` to disable a range.
            If `sent_range` is used, `word_range` is ignored.
        utterance_range : Tuple[int, int], optional
            Span of utterances before and after an utterance containing a matching
            word to include in the output.
            If set to ``(0, 0)`` (the default), no utterance range output is generated.
            If `utterance_range` is used, `word_range` is ignored.
        sent_range : Tuple[int, int], optional
            [Deprecated; please use utterance_range instead]
        by_tokens : bool, optional
            If ``True`` (the default), words in the output are in the token form
            (i.e., with Jyutping and part-of-speech tags).
            Otherwise just words as text strings are returned.
        by_utterances : bool, optional
            If ``True`` (default is False), utterances containing matching words
            are returned. Otherwise, only matching words are returned.
        tagged : bool, optional
            [Deprecated; please use by_tokens instead]
        sents : bool, optional
            [Deprecated; please use by_utterances instead]
        participants : str or iterable[str], optional
            One or more participants to include in the search.
            If unspecified, all participants are included.
        exclude : str or iterable[str], optional
            One or more participants to exclude in the search.
            If unspecified, no participants are excluded.
        by_files : bool, optional
            If True (default: False), return data organized by the
            individual file paths.

        Returns
        -------
        list
        """
        if sent_range != (0, 0):
            _deprecate("sent_range", "utterance_range", "3.2.0", "4.0.0")
            if utterance_range != (0, 0):
                raise TypeError(
                    "Do not use both utterance_range and sent_range "
                    f"(you've passed in {utterance_range} and {sent_range}, "
                    f"respectively). "
                    f"Please use utterance_range; "
                    f"sent_range has been deprecated."
                )
            utterance_range = sent_range
        if tagged is not None:
            _deprecate("tagged", "by_tokens", "3.2.0", "4.0.0")
            by_tokens = tagged
        if sents is not None:
            _deprecate("sents", "by_utterances", "3.2.0", "4.0.0")
            by_utterances = sents

        tagged_sents = self.tokens(
            participants=participants,
            exclude=exclude,
            by_utterances=True,
            by_files=True,
        )
        result_by_files = _perform_search(
            tagged_sents,
            onset=onset,
            nucleus=nucleus,
            coda=coda,
            tone=tone,
            initial=initial,
            final=final,
            jyutping=jyutping,
            character=character,
            pos=pos,
            word_range=word_range,
            utterance_range=utterance_range,
            by_tokens=by_tokens,
            by_utterances=by_utterances,
        )

        if by_files:
            return result_by_files
        else:
            return self._flatten(list, result_by_files)

    def _to_strs(self):
        strs = []
        for f in self._files:
            chat_str = ""
            for u in f.utterances:
                for mark, tier in u.tiers.items():
                    mark = mark if mark.startswith("%") else f"*{mark}"
                    chat_str += f"{mark}:\t{tier}\n"
            strs.append(chat_str)
        return strs


class _HKCanCorReader(CHATReader):
    """Corpus reader for HKCanCor specifically.

    We enforce uppercase for part-of-speech tags,
    because the original HKCanCor's tags have a mix of upper- and lowercase, e.g.,
    v and Vg, which makes it harder to perform a corpus search
    with a clean(er) regex.
    """

    @staticmethod
    def _preprocess_pos(pos: str) -> str:
        """Override the parent Reader class's method."""
        try:
            return pos.upper()
        except AttributeError:
            return pos


@functools.lru_cache(maxsize=1)
def hkcancor() -> CHATReader:
    """Create a corpus object for the Hong Kong Cantonese Corpus.

    Returns
    -------
    :class:`~pycantonese.CHATReader`
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data", "hkcancor")
    reader = _HKCanCorReader.from_dir(data_dir)
    for f in reader._files:
        f.file_path = f.file_path.replace(data_dir, "").lstrip(os.sep)
    return reader


@_params_in_docstring("match", "exclude", "encoding", class_method=False)
def read_chat(
    path: str, match: str = None, exclude: str = None, encoding: str = _ENCODING
) -> CHATReader:
    """Read Cantonese CHAT data files.

    Parameters
    ----------
    path : str
        A path that points to one of the following:

        - ZIP file. Either a local ``.zip`` file path or a URL (one that begins with
          ``"https://"`` or ``"http://"``).
          URL example: ``"https://childes.talkbank.org/data/Biling/YipMatthews.zip"``
        - A local directory, for files under this directory recursively.
        - A single ``.cha`` CHAT file.

    Returns
    -------
    :class:`~pycantonese.CHATReader`
    """
    return pylangacq_read_chat(
        path, match=match, exclude=exclude, encoding=encoding, cls=CHATReader
    )
