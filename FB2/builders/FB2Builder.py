import xml.etree.ElementTree as ET
from base64 import b64encode
from datetime import datetime
from typing import List, Tuple
from xml.dom import minidom

try:
    from .FictionBook2 import FictionBook2
except ImportError:
    import sys
    FictionBook2 = sys.modules[__package__ + '.FictionBook2']


class FB2Builder:
    book: FictionBook2

    def __init__(self, book: FictionBook2):
        self.book = book

    def GetFB2(self) -> ET.Element:
        fb2Tree = ET.Element("FictionBook", attrib={
            "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
            "xmlns:xlink": "http://www.w3.org/1999/xlink"
        })
        self._AddDescription(fb2Tree)
        self._AddBody(fb2Tree)
        self._AddBinaries(fb2Tree)
        return fb2Tree

    def _AddDescription(self, root: ET.Element) -> None:
        description = ET.SubElement(root, "description")
        self._AddTitleInfo(description)
        self._AddDocumentInfo(description)

    def _AddTitleInfo(self, description: ET.Element) -> None:
        titleInfo = ET.SubElement(description, "title-info")
        for genre in self.book.genres:
            ET.SubElement(titleInfo, "genre").text = genre
        for author in self.book.authors:
            titleInfo.append(self.BuildAuthorNameFromStr("author", author))
        ET.SubElement(titleInfo, "book-title").text = self.book.title
        if self.book.annotation is not None:
            annotationElement = ET.SubElement(titleInfo, "annotation")
            for paragraph in self.book.annotation.split("\n"):
                ET.SubElement(annotationElement, "p").text = paragraph
        if self.book.keywords is not None:
            ET.SubElement(titleInfo, "keywords").text = (
                "\n".join(self.book.keywords))
        if self.book.date is not None:
            dateElement = ET.SubElement(titleInfo, "date")
            dateElement.attrib["value"] = datetime.strftime(
                self.book.date, "%Y-%m-%d")
            dateElement.text = self.book.date.strftime("%Y-%m-%d")
        if self.book.coverPageImages is not None:
            coverPageElement = ET.SubElement(titleInfo, "coverpage")
            for i in range(len(self.book.coverPageImages)):
                imageElement = ET.SubElement(coverPageElement, "image")
                imageElement.attrib["xlink:href"] = f"#cover#{i}"
                imageElement.attrib["alt"] = "cover"
        ET.SubElement(titleInfo, "lang").text = self.book.lang
        if self.book.srcLang is not None:
            ET.SubElement(titleInfo, "src-lang").text = self.book.srcLang
        if self.book.translators is not None:
            for translator in self.book.translators:
                titleInfo.append(
                    self.BuildAuthorNameFromStr("translator", translator))
        if self.book.sequences is not None:
            sequence: Tuple[str, int]
            for sequence in self.book.sequences:
                ET.SubElement(titleInfo, "sequence", attrib={
                    "name": sequence[0],
                    "number": str(sequence[1])
                })

    def _AddDocumentInfo(self, description: ET.Element) -> None:
        documentInfo = ET.SubElement(description, "document-info")
        for author in self.book.docAuthors:
            documentInfo.append(self.BuildAuthorNameFromStr("author", author))
        ET.SubElement(documentInfo, "program-used").text = (
            "FB2creator by Ae-Mc")
        dateElement = ET.SubElement(documentInfo, "date")
        dateElement.text = datetime.now().strftime("%Y-%m-%d")
        dateElement.attrib["value"] = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(documentInfo, "id").text = self.book.docId
        ET.SubElement(documentInfo, "version").text = self.book.docVersion

    def _AddBody(self, root: ET.Element) -> None:
        if len(self.book.chapters):
            bodyElement = ET.SubElement(root, "body")
            for chapter in self.book.chapters:
                bodyElement.append(self.BuildSectionFromChapter(chapter))

    @staticmethod
    def BuildSectionFromChapter(chapter: Tuple[str, List[str]]) -> ET.Element:
        sectionElement = ET.Element("section")
        ET.SubElement(sectionElement, "title").text = chapter[0]
        for paragraph in chapter[1]:
            ET.SubElement(sectionElement, "p").text = paragraph
        return sectionElement

    def _AddBinaries(self, root: ET.Element) -> None:
        if self.book.coverPageImages is not None:
            for i, coverImage in enumerate(self.book.coverPageImages):
                self._AddBinary(root, f"cover#{i}", "image/jpeg", coverImage)

    def _AddBinary(self,
                   root: ET.Element,
                   id: str,
                   contentType: str,
                   data: bytes) -> None:
        binaryElement = ET.SubElement(root, "binary")
        binaryElement.attrib = {"id": id, "content-type": contentType}
        binaryElement.text = b64encode(data).decode("utf-8")

    @staticmethod
    def BuildAuthorNameFromStr(rootTag: str, name: str) -> ET.Element:
        rootElement = ET.Element(rootTag)
        authorNameParts = name.split(' ')
        if len(authorNameParts) == 1:
            ET.SubElement(rootElement, "nickname").text = (
                authorNameParts[0])
        elif len(authorNameParts) == 2:
            ET.SubElement(rootElement, "first-name").text = (
                authorNameParts[0])
            ET.SubElement(rootElement, "last-name").text = (
                authorNameParts[1])
        elif len(authorNameParts) == 3:
            ET.SubElement(rootElement, "first-name").text = (
                authorNameParts[0])
            ET.SubElement(rootElement, "last-name").text = (
                authorNameParts[1])
            ET.SubElement(rootElement, "middle-name").text = (
                authorNameParts[2])
        return rootElement

    @staticmethod
    def _PrettifyXml(element: ET.Element) -> str:
        dom = minidom.parseString(ET.tostring(element, "utf-8"))
        return dom.toprettyxml(encoding="utf-8").decode("utf-8")
