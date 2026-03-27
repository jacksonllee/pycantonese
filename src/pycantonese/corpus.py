from __future__ import annotations

import functools
import itertools
import os
import re
import sys
from collections.abc import Sequence
from typing import cast

from pycantonese._rust import Chat as _RustChat, Token, Utterance
from pycantonese.search import _perform_search

_IS_WASM = sys.platform == "emscripten"


def _flatten(iterable):
    """Flatten one level of nesting."""
    return list(itertools.chain.from_iterable(iterable))


class CHAT:
    """A reader for Cantonese CHAT corpus data.

    This class wraps a Rust-backed CHAT parser and provides
    Cantonese-specific functionality such as Jyutping extraction,
    character-level access, and corpus search.
    """

    def __init__(
        self,
        chat: _RustChat | None = None,
    ):
        self._chat = chat if chat is not None else _RustChat()

    @classmethod
    def from_zip(
        cls,
        path: str | os.PathLike[str],
        *,
        match: str | None = None,
        extension=".cha",
        parallel=True,
        strict=True,
        mor_tier="%mor",
        gra_tier="%gra",
    ):
        """Read CHAT data from a ZIP file.

        Args:
            path (str or os.PathLike[str]): Path to the ZIP file.
            match (str, optional): Glob pattern to match filenames within the ZIP.
            extension (str, optional): File extension to match.
                Default is ``".cha"``.
            parallel (bool, optional): If True, parse files in parallel.
            strict (bool, optional): If True, enforce strict parsing.
            mor_tier (str or None, optional): Name of the dependent tier to treat
                as the morphology tier, e.g. ``"%mor"`` or ``"%xmor"``. Default is
                ``"%mor"``. Set to None to disable mor+gra handling.
            gra_tier (str or None, optional): Name of the dependent tier to treat
                as the grammatical relation tier, e.g. ``"%gra"`` or ``"%xgra"``.
                Default is ``"%gra"``. Set to None to disable mor+gra handling.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(
            _RustChat.from_zip(
                os.fspath(path),
                match=match,
                extension=extension,
                parallel=parallel,
                strict=strict,
                mor_tier=mor_tier,
                gra_tier=gra_tier,
            )
        )

    @classmethod
    def from_dir(
        cls,
        path: str | os.PathLike[str],
        *,
        match: str | None = None,
        extension=".cha",
        parallel=True,
        strict=True,
        mor_tier="%mor",
        gra_tier="%gra",
    ):
        """Read CHAT data from a directory.

        Args:
            path (str or os.PathLike[str]): Path to the directory.
            match (str, optional): Glob pattern to match filenames within
                the directory.
            extension (str, optional): File extension to match.
                Default is ``".cha"``.
            parallel (bool, optional): If True, parse files in parallel.
            strict (bool, optional): If True, enforce strict parsing.
            mor_tier (str or None, optional): Name of the dependent tier to treat
                as the morphology tier, e.g. ``"%mor"`` or ``"%xmor"``. Default is
                ``"%mor"``. Set to None to disable mor+gra handling.
            gra_tier (str or None, optional): Name of the dependent tier to treat
                as the grammatical relation tier, e.g. ``"%gra"`` or ``"%xgra"``.
                Default is ``"%gra"``. Set to None to disable mor+gra handling.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(
            _RustChat.from_dir(
                os.fspath(path),
                match=match,
                extension=extension,
                parallel=parallel,
                strict=strict,
                mor_tier=mor_tier,
                gra_tier=gra_tier,
            )
        )

    @classmethod
    def from_files(
        cls,
        paths: Sequence[str | os.PathLike[str]],
        *,
        parallel=True,
        strict=True,
        mor_tier="%mor",
        gra_tier="%gra",
    ):
        """Read CHAT data from file paths.

        Args:
            paths (Sequence[str | os.PathLike[str]]): Paths to CHAT files.
            parallel (bool, optional): If True, parse files in parallel.
            strict (bool, optional): If True, enforce strict parsing.
            mor_tier (str or None, optional): Name of the dependent tier to treat
                as the morphology tier, e.g. ``"%mor"`` or ``"%xmor"``. Default is
                ``"%mor"``. Set to None to disable mor+gra handling.
            gra_tier (str or None, optional): Name of the dependent tier to treat
                as the grammatical relation tier, e.g. ``"%gra"`` or ``"%xgra"``.
                Default is ``"%gra"``. Set to None to disable mor+gra handling.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(
            _RustChat.from_files(
                [os.fspath(p) for p in paths],
                parallel=parallel,
                strict=strict,
                mor_tier=mor_tier,
                gra_tier=gra_tier,
            )
        )

    @classmethod
    def from_strs(
        cls,
        strs,
        *,
        ids=None,
        parallel=True,
        strict=True,
        mor_tier="%mor",
        gra_tier="%gra",
    ):
        """Read CHAT data from strings.

        Args:
            strs (list[str]): CHAT-formatted strings.
            ids (list[str], optional): Identifiers for each string.
            parallel (bool, optional): If True, parse strings in parallel.
            strict (bool, optional): If True, enforce strict parsing.
            mor_tier (str or None, optional): Name of the dependent tier to treat
                as the morphology tier, e.g. ``"%mor"`` or ``"%xmor"``. Default is
                ``"%mor"``. Set to None to disable mor+gra handling.
            gra_tier (str or None, optional): Name of the dependent tier to treat
                as the grammatical relation tier, e.g. ``"%gra"`` or ``"%xgra"``.
                Default is ``"%gra"``. Set to None to disable mor+gra handling.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(
            _RustChat.from_strs(
                strs,
                ids=ids,
                parallel=parallel,
                strict=strict,
                mor_tier=mor_tier,
                gra_tier=gra_tier,
            )
        )

    @classmethod
    def from_git(
        cls,
        url: str,
        *,
        rev: str | None = None,
        depth: int | None = None,
        match: str | None = None,
        extension=".cha",
        cache_dir: str | os.PathLike[str] | None = None,
        force_download=False,
        parallel=True,
        strict=True,
        mor_tier="%mor",
        gra_tier="%gra",
    ):
        """Read CHAT data from a Git repository.

        Args:
            url (str): URL of the Git repository.
            rev (str, optional): Git revision (branch, tag, or commit hash).
            depth (int, optional): Clone depth for shallow clones.
            match (str, optional): Glob pattern to match filenames within
                the repository.
            extension (str, optional): File extension to match.
                Default is ``".cha"``.
            cache_dir (str or os.PathLike[str], optional): Directory to cache
                the cloned repository.
            force_download (bool, optional): If True, force re-download
                even if cached.
            parallel (bool, optional): If True, parse files in parallel.
            strict (bool, optional): If True, enforce strict parsing.
            mor_tier (str or None, optional): Name of the dependent tier to treat
                as the morphology tier, e.g. ``"%mor"`` or ``"%xmor"``. Default is
                ``"%mor"``. Set to None to disable mor+gra handling.
            gra_tier (str or None, optional): Name of the dependent tier to treat
                as the grammatical relation tier, e.g. ``"%gra"`` or ``"%xgra"``.
                Default is ``"%gra"``. Set to None to disable mor+gra handling.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(
            _RustChat.from_git(
                url,
                rev=rev,
                depth=depth,
                match=match,
                extension=extension,
                cache_dir=os.fspath(cache_dir) if cache_dir is not None else None,
                force_download=force_download,
                parallel=parallel,
                strict=strict,
                mor_tier=mor_tier,
                gra_tier=gra_tier,
            )
        )

    @classmethod
    def from_url(
        cls,
        url: str,
        *,
        match: str | None = None,
        extension=".cha",
        cache_dir: str | os.PathLike[str] | None = None,
        force_download=False,
        parallel=True,
        strict=True,
        mor_tier="%mor",
        gra_tier="%gra",
    ):
        """Read CHAT data from a URL pointing to a ZIP archive.

        Args:
            url (str): URL of the ZIP archive.
            match (str, optional): Glob pattern to match filenames within
                the archive.
            extension (str, optional): File extension to match.
                Default is ``".cha"``.
            cache_dir (str or os.PathLike[str], optional): Directory to cache
                the downloaded archive.
            force_download (bool, optional): If True, force re-download
                even if cached.
            parallel (bool, optional): If True, parse files in parallel.
            strict (bool, optional): If True, enforce strict parsing.
            mor_tier (str or None, optional): Name of the dependent tier to treat
                as the morphology tier, e.g. ``"%mor"`` or ``"%xmor"``. Default is
                ``"%mor"``. Set to None to disable mor+gra handling.
            gra_tier (str or None, optional): Name of the dependent tier to treat
                as the grammatical relation tier, e.g. ``"%gra"`` or ``"%xgra"``.
                Default is ``"%gra"``. Set to None to disable mor+gra handling.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(
            _RustChat.from_url(
                url,
                match=match,
                extension=extension,
                cache_dir=os.fspath(cache_dir) if cache_dir is not None else None,
                force_download=force_download,
                parallel=parallel,
                strict=strict,
                mor_tier=mor_tier,
                gra_tier=gra_tier,
            )
        )

    @classmethod
    def from_utterances(cls, utterances):
        """Construct a CHAT reader from a list of utterances.

        Creates a new reader containing a single virtual file with the given
        utterances. Useful for splitting a reader into sub-readers based on
        utterance boundaries.

        Args:
            utterances (Sequence[Utterance]): Utterance objects to include.

        Returns:
            :class:`~pycantonese.CHAT`
        """
        return cls(_RustChat.from_utterances(utterances))

    def __getattr__(self, name):
        return getattr(self._chat, name)

    def tokens(
        self,
        *,
        by_utterance=False,
        by_file=False,
    ) -> list[Token] | list[list[Token]] | list[list[list[Token]]]:
        """Return the tokens.

        Args:
            by_utterance (bool, optional): If True, return tokens grouped
                by utterance.
            by_file (bool, optional): If True, return tokens grouped by file.

        Returns:
            list
        """
        return self._chat.tokens(
            by_utterance=by_utterance,
            by_file=by_file,
        )

    def words(
        self,
        *,
        by_utterance=False,
        by_file=False,
    ) -> list[str] | list[list[str]] | list[list[list[str]]]:
        """Return the words.

        Args:
            by_utterance (bool, optional): If True, return words grouped
                by utterance.
            by_file (bool, optional): If True, return words grouped by file.

        Returns:
            list
        """
        return self._chat.words(by_utterance=by_utterance, by_file=by_file)

    def jyutping(
        self,
        *,
        by_utterance=False,
        by_file=False,
    ) -> list[str | None] | list[list[str | None]] | list[list[list[str | None]]]:
        """Return the data in Jyutping romanization.

        Args:
            by_utterance (bool, optional): If True, return Jyutping grouped
                by utterance.
            by_file (bool, optional): If True, return Jyutping grouped by file.

        Returns:
            list
        """
        return self._chat.jyutping(by_utterance=by_utterance, by_file=by_file)

    @staticmethod
    def _get_chars_from_sent(sent: list[str]) -> list[str]:
        result = []
        for word in sent:
            if word and "\u4e00" <= word[0] <= "\u9fff":
                result.extend(list(word))
            else:
                result.append(word)
        return result

    def characters(
        self,
        *,
        by_utterance=False,
        by_file=False,
    ) -> list[str] | list[list[str]] | list[list[list[str]]]:
        """Return the data in individual Chinese characters.

        Args:
            by_utterance (bool, optional): If True, return characters grouped
                by utterance.
            by_file (bool, optional): If True, return characters grouped
                by file.

        Returns:
            list
        """
        sents = cast(
            list[list[list[str]]],
            self.words(by_utterance=True, by_file=True),
        )
        result = [
            [self._get_chars_from_sent(sent) for sent in sents_for_file]
            for sents_for_file in sents
        ]
        if by_file and by_utterance:
            pass
        elif by_file and not by_utterance:
            result = [_flatten(f) for f in result]
        elif not by_file and by_utterance:
            result = _flatten(result)
        else:
            result = _flatten(_flatten(f) for f in result)
        return result

    def word_ngrams(self, n: int):
        """Return word n-grams across all utterances.

        N-grams do not cross utterance boundaries.

        Args:
            n (int): The n-gram order (1 for unigrams, 2 for bigrams, etc.).

        Returns:
            Ngrams
        """
        return self._chat.word_ngrams(n)

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
        by_token=True,
        by_utterance=False,
        by_file=False,
    ):
        """Search the data for the given criteria.

        Args:
            onset (str, optional): Onset to search for. A regex is supported.
            nucleus (str, optional): Nucleus to search for.
                A regex is supported.
            coda (str, optional): Coda to search for. A regex is supported.
            tone (str, optional): Tone to search for. A regex is supported.
            initial (str, optional): Initial to search for.
                A regex is supported.
            final (str, optional): Final to search for.
            jyutping (str, optional): Jyutping romanization of one Cantonese
                character to search for.
            character (str, optional): One or more Cantonese characters to
                search for.
            pos (str, optional): A part-of-speech tag to search for.
                A regex is supported.
            word_range (tuple[int, int], optional): Span of words around
                a match. Default is ``(0, 0)``.
            utterance_range (tuple[int, int], optional): Span of utterances
                around a match. Default is ``(0, 0)``.
            by_token (bool, optional): If True, return Token objects.
                Otherwise return word strings.
            by_utterance (bool, optional): If True, return full utterances
                containing matches.
            by_file (bool, optional): If True, return data organized by file.

        Returns:
            list
        """
        tagged_sents = self.tokens(
            by_utterance=True,
            by_file=True,
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
            by_token=by_token,
            by_utterance=by_utterance,
        )

        if by_file:
            return result_by_files
        else:
            return _flatten(result_by_files)

    def utterances(self, *, by_file=False) -> list[Utterance] | list[list[Utterance]]:
        """Return the utterances.

        Args:
            by_file (bool, optional): If True, return utterances grouped
                by file.

        Returns:
            list[Utterance] | list[list[Utterance]]
        """
        return self._chat.utterances(by_file=by_file)

    def to_strs(self):
        """Return the data as CHAT-formatted strings.

        Returns:
            list[str]
        """
        return self._chat.to_strs()

    def to_files(self, dir_path: str | os.PathLike[str], *, filenames=None):
        """Write CHAT (.cha) files to a directory.

        Args:
            dir_path (str or os.PathLike[str]): Output directory path.
            filenames (list[str], optional): Filenames for each file.
        """
        self._chat.to_files(os.fspath(dir_path), filenames=filenames)

    @property
    def n_files(self):
        """The number of files."""
        return self._chat.n_files

    @property
    def file_paths(self):
        """The file paths."""
        return self._chat.file_paths

    def filter(self, *, participants=None, files=None):
        """Filter the data by participants and/or files.

        Args:
            participants (str, optional): Regex pattern to match participant
                codes.
            files (str, optional): Glob pattern to match file paths.

        Returns:
            CHAT
        """
        filtered = self._chat.filter(participants=participants, files=files)
        return CHAT(filtered)

    def append(self, other):
        """Append another CHAT object's data."""
        self._chat.append(other._chat)

    def extend(self, others):
        """Extend with data from multiple CHAT objects."""
        self._chat.extend([o._chat for o in others])

    def info(self, verbose=False):
        """Print summary information."""
        self._chat.info(verbose=verbose)

    def headers(self):
        """Return the headers."""
        return self._chat.headers()

    def participants(self, *, by_file=False):
        """Return the participants."""
        return self._chat.participants(by_file=by_file)

    def ages(self):
        """Return the ages."""
        return self._chat.ages()

    def head(self, n=5):
        """Return the first n utterances with a formatted display."""
        return self._chat.head(n=n)

    def tail(self, n=5):
        """Return the last n utterances with a formatted display."""
        return self._chat.tail(n=n)

    def languages(self, *, by_file=False):
        """Return the languages."""
        return self._chat.languages(by_file=by_file)


@functools.lru_cache(maxsize=1)
def hkcancor() -> CHAT:
    """Create a corpus object for the Hong Kong Cantonese Corpus.

    Returns:
        :class:`~pycantonese.CHAT`
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data", "hkcancor")
    chat = _RustChat.from_dir(data_dir, parallel=not _IS_WASM)
    return CHAT(chat)


@functools.lru_cache(maxsize=1)
def cantomap() -> CHAT:
    """Create a corpus object for the CantoMap corpus.

    Returns:
        :class:`~pycantonese.CHAT`
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data", "cantomap", "extracted")
    chat = _RustChat.from_dir(data_dir, parallel=not _IS_WASM)
    return CHAT(chat)


def _normalize_filter(
    value: str | Sequence[str] | None,
) -> str | None:
    """Convert a filter value to a single regex pattern string."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return "|".join(re.escape(v) for v in value)


def read_chat(
    path: str | os.PathLike[str],
    *,
    filter_files: str | Sequence[str] | None = None,
    filter_participants: str | Sequence[str] | None = None,
    strict: bool = True,
) -> CHAT:
    """Read Cantonese CHAT data files.

    Args:
        path (str or os.PathLike[str]): A path that points to one of the
            following:

            - A local ``.zip`` file path.
            - A local directory, for files under this directory recursively.
            - A single ``.cha`` CHAT file.

        filter_files (str or Sequence[str], optional): Filename(s) to keep.
            Regular expression matching is supported.
            If ``None``, all files are included.
        filter_participants (str or Sequence[str], optional): Participant
            code(s) to keep. Regular expression matching is supported.
            If ``None``, all participants are included.
        strict (bool, optional): If ``True``, enforce strict parsing of the
            CHAT data.

    Returns:
        :class:`~pycantonese.CHAT`
    """
    path = os.fspath(path)
    parallel = not _IS_WASM
    if path.endswith(".zip"):
        chat = _RustChat.from_zip(path, parallel=parallel, strict=strict)
    elif os.path.isdir(path):
        chat = _RustChat.from_dir(path, parallel=parallel, strict=strict)
    else:
        chat = _RustChat.from_files([path], parallel=parallel, strict=strict)
    files_pattern = _normalize_filter(filter_files)
    participants_pattern = _normalize_filter(filter_participants)
    if files_pattern is not None or participants_pattern is not None:
        chat = chat.filter(files=files_pattern, participants=participants_pattern)
    return CHAT(chat)
