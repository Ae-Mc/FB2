from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple, Union

from .Author import Author


@dataclass
class TitleInfo:
    genres: List[str] = field(default_factory=list)
    authors: List[Union[Author, str]] = field(default_factory=list)
    title: str = ""
    annotation: Optional[str] = None
    keywords: Optional[List[str]] = None
    date: Optional[Tuple[datetime, Optional[str]]] = None
    coverPageImages: Optional[List[bytes]] = None
    lang: str = "en"
    srcLang: Optional[str] = None
    translators: Optional[List[Union[Author, str]]] = None
    sequences: Optional[List[Tuple[str, int]]] = None
