import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Sequence, Tuple, Union
from uuid import uuid4

from .Author import Author


@dataclass
class DocumentInfo:
    authors: List[Union[Author, str]] = field(default_factory=list)
    programUsed: Optional[str] = "Ae-Mc's FB2 library"
    date: Tuple[datetime, Optional[str]] = (datetime.now(), None)
    sourceUrl: Optional[str] = None
    sourceAuthor: Optional[Union[Author, str]] = None
    id: str = field(default_factory=lambda: uuid4().hex)
    version: Union[Decimal, str] = Decimal("1.0")
    history: Optional[Union[str, Sequence[ET.Element]]] = None
    publisher: Optional[Union[Author, str]] = None
    """Holds information about document such as version, used program, etc.

    Attributes:
        authors: document authors
        programUsed: program that book was created with
        date: document creation date
        sourceUrl: original document url (if exists)
        sourceAuthor:original document author (if exists)
        id: document unique identificator
        version: document version
        history: document changelog in free format
        publisher: publisher name if exists
    """
