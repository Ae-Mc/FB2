import xml.etree.ElementTree as ET
from base64 import b64encode
from typing import List, Tuple
from xml.dom import minidom

from .builders import TitleInfoBuilder, DocumentInfoBuilder
from .TitleInfo import TitleInfo
from .FictionBook2dataclass import FictionBook2dataclass


class FB2Builder:
    book: FictionBook2dataclass
    """Transforms FictionBook2 to xml (fb2) format"""

    def __init__(self, book: FictionBook2dataclass):
        self.book = book

    def GetFB2(self) -> ET.Element:
        fb2Tree = ET.Element("FictionBook", attrib={
            "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
            "xmlns:xlink": "http://www.w3.org/1999/xlink"
        })
        self._AddStylesheets(fb2Tree)
        self._AddCustomInfos(fb2Tree)
        self._AddDescription(fb2Tree)
        self._AddBody(fb2Tree)
        self._AddBinaries(fb2Tree)
        return fb2Tree

    def _AddStylesheets(self, root: ET.Element) -> None:
        if self.book.stylesheets:
            for stylesheet in self.book.stylesheets:
                ET.SubElement(root, "stylesheet").text = stylesheet

    def _AddCustomInfos(self, root: ET.Element) -> None:
        if self.book.customInfos:
            for customInfo in self.book.customInfos:
                ET.SubElement(root, "custom-info").text = customInfo

    def _AddDescription(self, root: ET.Element) -> None:
        description = ET.SubElement(root, "description")
        self._AddTitleInfo("title-info", self.book.titleInfo, description)
        if self.book.sourceTitleInfo is not None:
            self._AddTitleInfo(
                "src-title-info", self.book.sourceTitleInfo, description)
        self._AddDocumentInfo(description)

    def _AddTitleInfo(self,
                      rootElement: str,
                      titleInfo: TitleInfo,
                      description: ET.Element) -> None:
        builder = TitleInfoBuilder(rootTag=rootElement, titleInfo=titleInfo)
        if titleInfo.coverPageImages:
            builder.AddCoverImages([f"#{rootElement}-cover_{i}" for i in range(
                len(titleInfo.coverPageImages))])
        description.append(builder.GetResult())

    def _AddDocumentInfo(self, description: ET.Element) -> None:
        description.append(DocumentInfoBuilder(
            documentInfo=self.book.documentInfo).GetResult())

    def _AddBody(self, root: ET.Element) -> None:
        if len(self.book.chapters):
            bodyElement = ET.SubElement(root, "body")
            for chapter in self.book.chapters:
                bodyElement.append(self.BuildSectionFromChapter(chapter))

    @staticmethod
    def BuildSectionFromChapter(chapter: Tuple[str, List[str]]) -> ET.Element:
        sectionElement = ET.Element("section")
        title = ET.SubElement(sectionElement, "title")
        ET.SubElement(title, "p").text = chapter[0]
        for paragraph in chapter[1]:
            ET.SubElement(sectionElement, "p").text = paragraph
        return sectionElement

    def _AddBinaries(self, root: ET.Element) -> None:
        if self.book.titleInfo.coverPageImages is not None:
            for i, coverImage in enumerate(
                    self.book.titleInfo.coverPageImages):
                self._AddBinary(
                    root, f"title-info-cover_{i}", "image/jpeg", coverImage)
        if (self.book.sourceTitleInfo
                and self.book.sourceTitleInfo.coverPageImages):
            for i, coverImage in enumerate(
                    self.book.sourceTitleInfo.coverPageImages):
                self._AddBinary(root,
                                f"src-title-info-cover#{i}",
                                "image/jpeg",
                                coverImage)

    def _AddBinary(self,
                   root: ET.Element,
                   id: str,
                   contentType: str,
                   data: bytes) -> None:
        binaryElement = ET.SubElement(root, "binary")
        binaryElement.attrib = {"id": id, "content-type": contentType}
        binaryElement.text = b64encode(data).decode("utf-8")

    @staticmethod
    def _PrettifyXml(element: ET.Element) -> str:
        dom = minidom.parseString(ET.tostring(element, "utf-8"))
        return dom.toprettyxml(encoding="utf-8").decode("utf-8")
