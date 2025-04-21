import xml.etree.ElementTree as ET
from base64 import b64encode
from xml.dom import minidom

from FB2.Chapter import BaseChapter, ChapterWithSubchapters, SimpleChapter

from .builders import DocumentInfoBuilder, TitleInfoBuilder
from .FictionBook2dataclass import FictionBook2dataclass
from .Image import Image
from .TitleInfo import TitleInfo


class FB2Builder:
    book: FictionBook2dataclass
    """Transforms FictionBook2 to xml (fb2) format"""

    def __init__(self, book: FictionBook2dataclass):
        self.book = book

    def GetFB2(self) -> ET.Element:
        fb2Tree = ET.Element(
            "FictionBook",
            attrib={
                "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
            },
        )
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
            self._AddTitleInfo("src-title-info", self.book.sourceTitleInfo, description)
        self._AddDocumentInfo(description)

    def _AddTitleInfo(
        self, rootElement: str, titleInfo: TitleInfo, description: ET.Element
    ) -> None:
        builder = TitleInfoBuilder(rootTag=rootElement, titleInfo=titleInfo)
        description.append(builder.GetResult())

    def _AddDocumentInfo(self, description: ET.Element) -> None:
        description.append(
            DocumentInfoBuilder(documentInfo=self.book.documentInfo).GetResult()
        )

    def _AddBody(self, root: ET.Element) -> None:
        if len(self.book.chapters):
            bodyElement = ET.SubElement(root, "body")
            ET.SubElement(
                ET.SubElement(bodyElement, "title"), "p"
            ).text = self.book.titleInfo.title
            if not all(
                [isinstance(chapter, BaseChapter) for chapter in self.book.chapters]
            ):
                raise ValueError(
                    "All chapters must be derived from BaseChapter (SimpleChapter or ChapterWithSubchapters)."
                )
            for chapter in self.book.chapters:
                bodyElement.append(self._BuildSectionFromChapter(chapter))

    def _BuildSectionFromChapter(
        self,
        chapter: BaseChapter,
    ) -> ET.Element:
        sectionElement = ET.Element("section")
        if isinstance(chapter.title, str):
            ET.SubElement(
                ET.SubElement(sectionElement, "title"), "p"
            ).text = chapter.title
        else:
            sectionElement.append(chapter.title)
        if chapter.image:
            ET.SubElement(
                sectionElement,
                "image",
                attrib={"xlink:href": f"#{chapter.image.uid}"},
            )
            self.book.images.append(chapter.image)
        if chapter.epigraph:
            epigraph = ET.SubElement(sectionElement, "epigraph")
            for element in chapter.epigraph:
                ET.SubElement(epigraph, "p").text = element
        if chapter.annotation:
            annotation = ET.SubElement(sectionElement, "annotation")
            for element in chapter.annotation:
                ET.SubElement(annotation, "p").text = element
        if isinstance(chapter, SimpleChapter):
            for element in chapter.content:
                if isinstance(element, str):
                    ET.SubElement(sectionElement, "p").text = element
                elif isinstance(element, Image):
                    self.book.images.append(element)
                    ET.SubElement(
                        sectionElement,
                        "image",
                        attrib={"xlink:href": f"#{element.uid}"},
                    )
                elif isinstance(element, ET.Element):
                    sectionElement.append(element)
                else:
                    raise ValueError(
                        "Unknown section subelement type (supported: str, FB2.Image,"
                        f" xml.etree.ElementTree.Element): {type(element)}"
                    )
        elif isinstance(chapter, ChapterWithSubchapters):
            for subchapter in chapter.subchapters:
                sectionElement.append(self._BuildSectionFromChapter(subchapter))
        else:
            raise ValueError(
                "Wrong chapter structure: second element of chapter tuple must be list!"
            )

        return sectionElement

    def _AddBinaries(self, root: ET.Element) -> None:
        if self.book.titleInfo.coverPageImages is not None:
            for coverImage in self.book.titleInfo.coverPageImages:
                self._AddBinary(
                    root, coverImage.uid, coverImage.media_type, coverImage.content
                )
        if self.book.sourceTitleInfo and self.book.sourceTitleInfo.coverPageImages:
            for coverImage in self.book.sourceTitleInfo.coverPageImages:
                self._AddBinary(
                    root, coverImage.uid, coverImage.media_type, coverImage.content
                )
        for image in self.book.images:
            self._AddBinary(root, image.uid, image.media_type, image.content)

    def _AddBinary(
        self, root: ET.Element, id: str, contentType: str, data: bytes
    ) -> None:
        ET.SubElement(
            root, "binary", {"id": id, "content-type": contentType}
        ).text = b64encode(data).decode("utf-8")

    @staticmethod
    def _PrettifyXml(element: ET.Element) -> str:
        dom = minidom.parseString(ET.tostring(element, "utf-8"))
        return dom.toprettyxml(encoding="utf-8").decode("utf-8")
