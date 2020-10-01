from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import uuid4
from .FB2Builder import FB2Builder


@dataclass
class FictionBook2():
    genres: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    title: str = ""
    annotation: Optional[str] = None
    keywords: Optional[List[str]] = None
    date: Optional[datetime] = None
    coverPageImages: Optional[List[bytes]] = None
    lang: str = "en"
    srcLang: Optional[str] = None
    translators: Optional[List[str]] = None
    sequences: Optional[List[Tuple[str, int]]] = None
    docAuthors: List[str] = field(default_factory=list)
    docId: str = str(uuid4())
    docVersion: str = "1.0"
    chapters: List[Tuple[str, List[str]]] = field(default_factory=list)

    def write(self, filename: str):
        with open(filename, 'w') as f:
            f.write(str(self))

    def __str__(self) -> str:
        return FB2Builder._PrettifyXml(FB2Builder(self).GetFB2())
