from __future__ import annotations

from .characters import characters_to_jyutping
from .ipa import jyutping_to_ipa


def g2p(
    chars: str | list[str],
    *,
    onsets: dict[str, str] | None = None,
    nuclei: dict[str, str] | None = None,
    codas: dict[str, str] | None = None,
) -> list[tuple[str, list[str] | None]]:
    """Convert Cantonese characters into IPA (grapheme-to-phoneme).

    This is a one-shot grapheme-to-phoneme (G2P) helper that composes
    :func:`~pycantonese.characters_to_jyutping` and
    :func:`~pycantonese.jyutping_to_ipa`. The input is segmented into words
    (using :func:`~pycantonese.segment` if a raw string is passed), each word
    is mapped to Jyutping, and each Jyutping syllable is then mapped to IPA.

    Args:
        chars (str or list[str]): A string of Cantonese characters, in which
            case word segmentation is also run on this input string
            (by :func:`~pycantonese.segment`) in order to resolve potential
            ambiguity in mapping characters to Jyutping. If you don't want
            word segmentation to be done, then provide a list of strings
            instead with your desired segmentation.
        onsets (dict[str, str], optional): Custom Jyutping-onset to IPA-symbol
            overrides, forwarded to :func:`~pycantonese.jyutping_to_ipa`.
        nuclei (dict[str, str], optional): Custom Jyutping-nucleus to IPA-symbol
            overrides, forwarded to :func:`~pycantonese.jyutping_to_ipa`.
        codas (dict[str, str], optional): Custom Jyutping-coda to IPA-symbol
            overrides, forwarded to :func:`~pycantonese.jyutping_to_ipa`.

    Returns:
        list[tuple[str, list[str] | None]]: A list of segmented words, where
        each word is a 2-tuple of (Cantonese characters, list of IPA syllables).
        The IPA list contains one IPA string per character of the word.
        Any word with no Jyutping mapping (e.g. an unseen character or a
        punctuation mark) yields ``None`` in place of the IPA list.

    Examples:
        >>> g2p("香港人講廣東話。")  # Hongkongers speak Cantonese.
        [('香港人', ['hœŋ55', 'kɔŋ25', 'jɐn21']), ('講', ['kɔŋ25']), ('廣東話', ['kʷɔŋ25', 'tʊŋ55', 'waː25']), ('。', None)]

    See Also:
        :func:`~pycantonese.characters_to_jyutping`,
        :func:`~pycantonese.jyutping_to_ipa`.
    """  # noqa: E501
    result: list[tuple[str, list[str] | None]] = []
    for word, jp in characters_to_jyutping(chars):
        if jp is None:
            result.append((word, None))
        else:
            ipa = jyutping_to_ipa(
                jp,
                return_as="list",
                onsets=onsets,
                nuclei=nuclei,
                codas=codas,
            )
            assert isinstance(ipa, list)
            result.append((word, ipa))
    return result
