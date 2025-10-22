import xml.etree.ElementTree as ET
from typing import Sequence

from pydantic import BaseModel, Field

from FB2.Chapter import BaseChapter
from FB2.DocumentInfo import DocumentInfo
from FB2.FB2Builder import FB2Builder
from FB2.Image import Image
from FB2.TitleInfo import TitleInfo


class FictionBook2(BaseModel):
    """Represents fb2 book

    Attributes:
        stylesheets: optional css styles
        titleInfo: book title information
        sourceTitleInfo: source book title information (if exists)
        documentInfo: document information
        customInfos: free format additional information
        chapters: list of chapters names and lists of paragraphs or Elements
            with paragraphs or lists of Elements
        images: list of images
    """

    stylesheets: Sequence[str] | None = None
    titleInfo: TitleInfo = Field(default_factory=TitleInfo)
    sourceTitleInfo: TitleInfo | None = None
    documentInfo: DocumentInfo = Field(default_factory=DocumentInfo)
    customInfos: Sequence[str] | None = None
    chapters: Sequence[BaseChapter] = Field(default_factory=list[BaseChapter])
    images: Sequence[Image] = Field(default_factory=list[Image])

    def write(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(self))

    def tostring(self: "FictionBook2", prettify: bool) -> str:
        if prettify:
            return FB2Builder.PrettifyXml(FB2Builder(self).GetFB2())
        return ET.tostring(FB2Builder(self).GetFB2()).decode("utf-8")

    def __str__(self) -> str:
        return self.tostring(prettify=True)
