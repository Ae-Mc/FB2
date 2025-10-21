from datetime import datetime
from typing import Sequence

from pydantic import BaseModel, Field

from FB2.Author import Author
from FB2.Image import Image


class TitleInfo(BaseModel):
    """Holds book info such as title, annotation, genres, authors, etc.

    Attributes:
        title: book title
        authors: book authors
        annotation: book annotation
        genres: book genres
        keywords: book keywords
        date: book publication date
        coverPageImages: list of Images with book cover images
        lang: book language code (iso639)
        srcLang: source book language code (if exists, iso639)
        translators: book translators (if exist)
        sequences: list of sequences names and book numbers in each sequence
    """

    title: str = "Untitled book"
    authors: Sequence[Author | str] = Field(
        default_factory=lambda: [Author(nickname="Unknown author")]
    )
    annotation: str | None = None
    genres: Sequence[str] = Field(default_factory=lambda: ["Unrecognized"])
    keywords: Sequence[str] | None = None
    date: tuple[datetime, str | None] | None = None
    coverPageImages: Sequence[Image] | None = None
    lang: str = "en"
    srcLang: str | None = None
    translators: Sequence[Author | str] | None = None
    sequences: Sequence[tuple[str, int]] | None = None
