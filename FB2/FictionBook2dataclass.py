from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from .TitleInfo import TitleInfo
from .DocumentInfo import DocumentInfo


@dataclass
class FictionBook2dataclass:
    """Represents fb2 book

    Attributes:
        stylesheets: optional css styles
        titleInfo: book title information
        sourceTitleInfo: source book title information (if exists)
        documentInfo: document information
        customInfos: free format additional information
        chapters: list of chapters names and lists of paragraphs
    """
    stylesheets: Optional[List[str]] = None
    titleInfo: TitleInfo = field(default_factory=TitleInfo)
    sourceTitleInfo: Optional[TitleInfo] = None
    documentInfo: DocumentInfo = field(default_factory=DocumentInfo)
    customInfos: Optional[List[str]] = None
    chapters: List[Tuple[str, List[str]]] = field(default_factory=list)
