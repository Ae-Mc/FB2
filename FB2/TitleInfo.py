from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple, Union

from .Author import Author
from .Image import Image


@dataclass
class TitleInfo:
    title: str = "Untitled book"
    authors: List[Union[Author, str]] = field(
        default_factory=lambda: [Author("Unknown author")]
    )
    annotation: Optional[str] = None
    genres: List[str] = field(default_factory=lambda: ["Unrecognized"])
    keywords: Optional[List[str]] = None
    date: Optional[Tuple[datetime, Optional[str]]] = None
    coverPageImages: Optional[List[Image]] = None
    lang: str = "en"
    srcLang: Optional[str] = None
    translators: Optional[List[Union[Author, str]]] = None
    sequences: Optional[List[Tuple[str, int]]] = None
    """Holds book info such as title, annotation, genres, authors, etc.

    Attributes:
        title: book title
        authors: book authors
        annotation: book annotation
        genres: book genres
        keywords: book keywords
        date: book publication date
        coverPageImages: list of Images with book cover images
        lang: book language code
        srcLang: source book language code (if exists)
        translators: book translators (if exist)
        sequences: list of sequences names and book numbers in each sequence
    """
