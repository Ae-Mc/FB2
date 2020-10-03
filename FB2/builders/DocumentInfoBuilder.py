import xml.etree.ElementTree as ET
from typing import Union, Sequence, Tuple
from datetime import datetime
from ..Author import Author
from ..DocumentInfo import DocumentInfo
from .BuildAuthorName import BuildAuthorName


class DocumentInfoBuilder:
    result: ET.Element

    def __init__(self, documentInfo: DocumentInfo = None):
        self.reset()

    def AddAuthors(self,
                   authors: Sequence[Union[Author, str, ET.Element]]) -> None:
        for author in authors:
            if isinstance(author, ET.Element):
                self.result.append(author)
            else:
                self.result.append(BuildAuthorName("author", author))

    def AddProgramUsed(self, programUsed: str):
        ET.SubElement(self.result, "program-used").text = programUsed

    def AddDate(self, date: Tuple[datetime, Optional[str]]) -> None:
        dateElement = ET.Element("date")
        dateElement.attrib["value"] = date[0].strftime("%Y-%m-%d")
        dateElement.text = date[1] or date[0].strftime("%d.%m.%Y")
        self.result.append(dateElement)

    def AddSourceUrl(self, sourceUrl: str):
        ET.SubElement(self.result, "src-url").text = sourceUrl

    def AddSourceAuthor(self, sourceAuthor: Union[Author, str]):
        self.result.append(BuildAuthorName("src-ocr", sourceAuthor))

    def reset(self):
        self.result = ET.Element("document-info")
