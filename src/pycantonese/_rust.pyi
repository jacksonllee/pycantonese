from __future__ import annotations

from typing import Any

from rustling.chat import Headers
from rustling.ngram import Ngrams

class Token:
    word: str
    pos: str | None
    jyutping: str | None
    mor: str | None
    gloss: str | None
    gra: Any | None

    def __init__(
        self,
        word: str,
        pos: str | None = None,
        jyutping: str | None = None,
        mor: str | None = None,
        gloss: str | None = None,
        gra: Any | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def to_mor_tier(self) -> str: ...
    def to_gra_tier(self) -> str: ...

class Utterance:
    participant: str
    tokens: list[Token]
    time_marks: tuple[int, int] | None
    tiers: dict[str, str]
    raw: str
    changeable_header: Any | None

    def __init__(
        self,
        *,
        participant: str,
        tokens: list[Token],
        time_marks: tuple[int, int] | None = None,
        tiers: dict[str, str] | None = None,
        raw: str = "",
        changeable_header: Any | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...

class Chat:
    def __init__(self) -> None: ...
    @classmethod
    def from_dir(
        cls,
        path: str,
        match: str | None = None,
        extension: str = ".cha",
        parallel: bool = True,
        strict: bool = True,
    ) -> Chat: ...
    @classmethod
    def from_files(
        cls,
        paths: list[str],
        parallel: bool = True,
        strict: bool = True,
    ) -> Chat: ...
    @classmethod
    def from_strs(
        cls,
        strs: list[str],
        ids: list[str] | None = None,
        parallel: bool = True,
        strict: bool = True,
    ) -> Chat: ...
    @classmethod
    def from_zip(
        cls,
        path: str,
        match: str | None = None,
        extension: str = ".cha",
        parallel: bool = True,
        strict: bool = True,
    ) -> Chat: ...
    @classmethod
    def from_utterances(cls, utterances: list[Utterance]) -> Chat: ...
    def tokens(self, *, by_utterance: bool = False, by_file: bool = False) -> Any: ...
    def jyutping(self, *, by_utterance: bool = False, by_file: bool = False) -> Any: ...
    def utterances(self, *, by_file: bool = False) -> Any: ...
    def words(self, *, by_utterance: bool = False, by_file: bool = False) -> Any: ...
    @property
    def n_files(self) -> int: ...
    @property
    def file_paths(self) -> list[str]: ...
    def filter(
        self, *, participants: str | None = None, files: str | None = None
    ) -> Chat: ...
    def to_strs(self) -> list[str]: ...
    def to_chat(
        self,
        path: str,
        *,
        is_dir: bool = False,
        filenames: list[str] | None = None,
    ) -> None: ...
    def append(self, other: Chat) -> None: ...
    def extend(self, others: list[Chat]) -> None: ...
    def headers(self) -> list[Headers]: ...
    def ages(self) -> list[Any]: ...
    def participants(self, *, by_file: bool = False) -> Any: ...
    def languages(self, *, by_file: bool = False) -> Any: ...
    def info(self, verbose: bool = False) -> None: ...
    def head(self, n: int = 5) -> None: ...
    def tail(self, n: int = 5) -> None: ...
    def word_ngrams(self, n: int) -> Ngrams: ...
    def __bool__(self) -> bool: ...
