from functools import lru_cache
import os

from pylangacq.chat import Reader

from pycantonese.search import perform_search
from pycantonese.util import ENCODING, get_jyutping_from_mor, ListFromIterables


class CantoneseCHATReader(Reader):
    """A reader for Cantonese CHAT corpus files.

    .. note:: Some of the methods are inherited from the parent class
        ``pylangacq.chat.Reader`` for language acquisition,
        which may or may not be applicable to your use case.
    """

    def __init__(self, *filenames, **kwargs):
        """Initialize a reader for Cantonese CHAT corpus files.

        Parameters
        ----------
        *filenames : iterable of str
            File paths to Cantonese CHAT data files. Glob filename matching
            is supported.
        **kwargs
            Keyword arguments passed to CantoneseCHATReader. Currently, only
            the ``encoding`` kwarg is supported (default: 'utf8').
        """
        encoding = kwargs.get("encoding", ENCODING)
        super(CantoneseCHATReader, self).__init__(
            *filenames, encoding=encoding
        )

    def concordance(
        self,
        search_item,
        participant=None,
        exclude=None,
        match_entire_word=True,
        lemma=False,
        by_files=False,
    ):
        raise NotImplementedError("coming soon!")

    def _get_jyutping_sents(self, participant=None, exclude=None, sents=True):
        fname_to_tagged_sents = self.tagged_sents(
            participant=participant, exclude=exclude, by_files=True
        )

        fn_to_jyutpings = {}
        jyutpings_list = []

        for fn in self.filenames():
            fn_to_jyutpings[fn] = []
            tagged_sents = fname_to_tagged_sents[fn]

            for tagged_sent in tagged_sents:
                if sents:
                    jyutpings_list = []

                for tagged_word in tagged_sent:
                    _, _, mor, _ = tagged_word
                    jyutping = get_jyutping_from_mor(mor)

                    if sents:
                        jyutpings_list.append(jyutping)
                    else:
                        fn_to_jyutpings[fn].append(jyutping)

                if sents:
                    fn_to_jyutpings[fn].append(jyutpings_list)

        return fn_to_jyutpings

    def jyutpings(self, participant=None, exclude=None, by_files=False):
        """Return the words in Jyutping romanization.

        Parameters
        ----------
        participant : str or iterable[str], optional
            One or more participants to include the data for.
            If unspecified, all participants are included.
        exclude : str or iterable[str], optional
            One or more participants to exclude the data for.
            If unspecified, no participants are excluded.
        by_files : bool, optional
            If True (default: False), return data organized by the
            individual file paths.

        Returns
        -------
        list[str], or dict[str, list[str]] if by_files is True
        """
        fn_to_jyutpings = self._get_jyutping_sents(
            participant=participant, exclude=exclude, sents=False
        )

        if by_files:
            return fn_to_jyutpings
        else:
            return ListFromIterables(
                *(v for _, v in sorted(fn_to_jyutpings.items()))
            )

    def jyutping_sents(self, participant=None, exclude=None, by_files=False):
        """Return the sentences in Jyutping romanization.

        Parameters
        ----------
        participant : str or iterable[str], optional
            One or more participants to include the data for.
            If unspecified, all participants are included.
        exclude : str or iterable[str], optional
            One or more participants to exclude the data for.
            If unspecified, no participants are excluded.
        by_files : bool, optional
            If True (default: False), return data organized by the
            individual file paths.

        Returns
        -------
        list[list[str]], or dict[str, list[list[str]]] if by_files is True
        """
        fn_to_jyutpings = self._get_jyutping_sents(
            participant=participant, exclude=exclude, sents=True
        )

        if by_files:
            return fn_to_jyutpings
        else:
            return ListFromIterables(
                *(v for _, v in sorted(fn_to_jyutpings.items()))
            )

    def _get_character_sents(self, participant=None, exclude=None, sents=True):
        fname_to_tagged_sents = self.tagged_sents(
            participant=participant, exclude=exclude, by_files=True
        )

        fn_to_characters = {}
        characters_list = []

        for fn in self.filenames():
            fn_to_characters[fn] = []
            tagged_sents = fname_to_tagged_sents[fn]

            for tagged_sent in tagged_sents:
                if sents:
                    characters_list = []

                for tagged_word in tagged_sent:
                    chs, _, _, _ = tagged_word

                    if chs and "\u4e00" <= chs[0] <= "\u9fff":
                        characters_in_word = list(chs)
                    else:
                        characters_in_word = [chs]

                    if sents:
                        characters_list.extend(characters_in_word)
                    else:
                        fn_to_characters[fn].extend(characters_in_word)

                if sents:
                    fn_to_characters[fn].append(characters_list)

        return fn_to_characters

    def characters(self, participant=None, exclude=None, by_files=False):
        """Return the data split in individual Cantonese characters.

        Parameters
        ----------
        participant : str or iterable[str], optional
            One or more participants to include the data for.
            If unspecified, all participants are included.
        exclude : str or iterable[str], optional
            One or more participants to exclude the data for.
            If unspecified, no participants are excluded.
        by_files : bool, optional
            If True (default: False), return data organized by the
            individual file paths.

        Returns
        -------
        list[str], or dict[str, list[str]] if by_files is True
        """
        fn_to_characters = self._get_character_sents(
            participant=participant, exclude=exclude, sents=False
        )

        if by_files:
            return fn_to_characters
        else:
            return ListFromIterables(
                *(v for _, v in sorted(fn_to_characters.items()))
            )

    def character_sents(self, participant=None, exclude=None, by_files=False):
        """Return the data as sentences of individual Cantonese characters.

        Parameters
        ----------
        participant : str or iterable[str], optional
            One or more participants to include the data for.
            If unspecified, all participants are included.
        exclude : str or iterable[str], optional
            One or more participants to exclude the data for.
            If unspecified, no participants are excluded.
        by_files : bool, optional
            If True (default: False), return data organized by the
            individual file paths.

        Returns
        -------
        list[list[str]], or dict[str, list[list[str]]] if by_files is True
        """
        fn_to_characters = self._get_character_sents(
            participant=participant, exclude=exclude, sents=True
        )

        if by_files:
            return fn_to_characters
        else:
            return ListFromIterables(
                *(v for _, v in sorted(fn_to_characters.items()))
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
        sent_range=(0, 0),
        tagged=True,
        sents=False,
        participant=None,
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
        sent_range : tuple[int, int], optional
            Span of sentences before and after a sentence containing a matching
            word to include in the output. The default is `(0, 0)` to disable
            a range. If `sent_range` is used, `word_range` is ignored.
        tagged : bool, optional
            If True (the default), words in the output are in the tagged form.
            Otherwise just word token strings are returned.
        sents : bool, optional
            If True (default is False), sentences containing matching words
            are returned. Otherwise, only matching words are returned.
        participant : str or iterable[str], optional
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
        tagged_sents = self.tagged_sents(
            participant=participant, exclude=exclude, by_files=True
        )
        fn_to_results = perform_search(
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
            sent_range=sent_range,
            tagged=tagged,
            sents=sents,
        )

        if by_files:
            return fn_to_results
        else:
            return ListFromIterables(
                *(v for _, v in sorted(fn_to_results.items()))
            )


@lru_cache(maxsize=1)
def hkcancor():
    """Create a corpus object for the Hong Kong Cantonese Corpus.

    Returns
    -------
    :class:`~pycantonese.corpus.CantoneseCHATReader`
    """
    data_path = os.path.join(
        os.path.dirname(__file__), "data", "hkcancor", "*.cha"
    )
    return CantoneseCHATReader(data_path, encoding="utf8")


def read_chat(*filenames, **kwargs):
    """Read Cantonese CHAT data files into a reader object.

    Parameters
    ----------
    *filenames : iterable[str]
        File paths to Cantonese CHAT data files. Glob filename matching
        is supported.
    **kwargs
        Keyword arguments passed to CantoneseCHATReader.
        Currently, only the ``encoding`` kwarg is supported (default: 'utf8').

    Returns
    -------
    :class:`~pycantonese.corpus.CantoneseCHATReader`
    """
    encoding = kwargs.get("encoding", ENCODING)
    return CantoneseCHATReader(*filenames, encoding=encoding)
