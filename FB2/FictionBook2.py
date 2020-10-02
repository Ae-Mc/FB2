from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
from uuid import uuid4

from .FB2Builder import FB2Builder
from .TitleInfo import TitleInfo
from .Author import Author


@dataclass
class FictionBook2():
    titleInfo: TitleInfo = field(default_factory=TitleInfo)
    sourceTitleInfo: Optional[TitleInfo] = None
    docAuthors: List[Union[Author, str]] = field(default_factory=list)
    docId: str = str(uuid4())
    docVersion: str = "1.0"
    chapters: List[Tuple[str, List[str]]] = field(default_factory=list)

    def write(self, filename: str):
        with open(filename, 'w') as f:
            f.write(str(self))

    def __str__(self) -> str:
        return FB2Builder._PrettifyXml(FB2Builder(self).GetFB2())
