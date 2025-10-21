import xml.etree.ElementTree as ET
from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field

from FB2.Image import Image


class BaseChapter(BaseModel):
    title: str | ET.Element
    image: Image | None = None
    epigraph: Sequence[str] | None = None
    annotation: Sequence[str] | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SimpleChapter(BaseChapter):
    """Holds chapter info such as title and content.

    Attributes:
        title: chapter title
        image: chapter cover
        epigraph: chapter epigraph
        annotation: chapter annotation
        content: list of strings (text), FB2.Image objects or xml.etree.ElementTree.Element objects
    """

    content: Sequence[str | Image | ET.Element] = Field(
        default_factory=list[str | Image | ET.Element]
    )


class ChapterWithSubchapters(BaseChapter):
    """Holds chapter info such as title and content.

    Attributes:
        title: chapter title
        image: chapter cover
        epigraph: chapter epigraph
        annotation: chapter annotation
        subchapters: list of subchapters (if exist)
    """

    subchapters: Sequence["SimpleChapter | ChapterWithSubchapters"] = Field(
        default_factory=list["SimpleChapter | ChapterWithSubchapters"]
    )
