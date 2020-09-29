from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import uuid4
from .FB2Builder import FB2Builder


@dataclass
class FictionBook2():
    genres: List[str] = ()
    authors: List[str] = ()
    title: str = ""
    annotation: Optional[str] = None
    keywords: Optional[List[str]] = None
    date: Optional[datetime] = None
    coverPageImages: Optional[List[bytes]] = None
    lang: str = "en"
    srcLang: Optional[str] = None
    translators: Optional[List[str]] = None
    sequences: Optional[List[Tuple[str, int]]] = None
    docAuthors: List[str] = ("Ae-Mc")
    docId: str = str(uuid4())
    docVersion: str = "1.0"
    chapters: List[Tuple[str, List[str]]] = ()

    def write(self, filename: str):
        with open(filename, 'w') as f:
            f.write(FB2Builder._PrettifyXml(FB2Builder(self).GetFB2()))
