import xml.etree.ElementTree as ET
from datetime import datetime
from decimal import Decimal
from typing import Sequence
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from FB2.Author import Author


class DocumentInfo(BaseModel):
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

    authors: Sequence[Author | str] = Field(default_factory=list[Author | str])
    programUsed: str | None = "Ae-Mc's FB2 library"
    date: tuple[datetime, str | None] = (datetime.now(), None)
    sourceUrl: str | None = None
    sourceAuthor: Author | str | None = None
    id: str = Field(default_factory=lambda: uuid4().hex)
    version: Decimal | str = Decimal("1.0")
    history: str | Sequence[ET.Element] | None = None
    publisher: Author | str | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
