import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional, Union

from FB2 import Image


@dataclass
class BaseChapter:
    title: Union[str, ET.Element]
    image: Optional[Image] = None
    epigraph: Optional[List[str]] = None
    annotation: Optional[List[str]] = None


@dataclass
class SimpleChapter(BaseChapter):
    """Holds chapter info such as title and content.

    Attributes:
        title: chapter title
        content: list of strings (text), FB2.Image objects or xml.etree.ElementTree.Element objects
    """

    content: List[Union[str, Image, ET.Element]] = field(default_factory=list)


@dataclass
class ChapterWithSubchapters(BaseChapter):
    """Holds chapter info such as title and content.

    Attributes:
        title: chapter title
        subchapters: list of subchapters (if exist)
    """

    subchapters: List[Union[SimpleChapter, "ChapterWithSubchapters"]] = field(
        default_factory=list
    )
