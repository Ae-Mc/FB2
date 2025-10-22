import xml.etree.ElementTree as ET
from base64 import b64encode
from typing import TYPE_CHECKING
from xml.dom import minidom

from FB2.builders import DocumentInfoBuilder, TitleInfoBuilder
from FB2.Chapter import BaseChapter, ChapterWithSubchapters, SimpleChapter
from FB2.ChapterContent import EmptyLine, Paragraph, ParagraphBase
from FB2.constants import FB2_LINK_PREFIX
from FB2.Image import Image
from FB2.TitleInfo import TitleInfo

if TYPE_CHECKING:
    from FB2.FictionBook2 import FictionBook2


class FB2Builder:
    """Transforms FictionBook2 to xml (fb2) format"""

    book: "FictionBook2"
    images: list[Image]

    def __init__(self, book: "FictionBook2"):
        self.book = book

    def GetFB2(self) -> ET.Element:
        fb2Tree = ET.Element(
            "FictionBook",
            attrib={
                "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
            },
        )
        self.images = list(self.book.images)
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
        self,
        rootElement: str,
        titleInfo: TitleInfo,
        description: ET.Element,
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
                attrib={f"{FB2_LINK_PREFIX}:href": f"#{chapter.image.uid}"},
            )
            self.images.append(chapter.image)
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
                match element:
                    case str():
                        ET.SubElement(sectionElement, "p").text = element
                    case Image():
                        self.images.append(element)
                        ET.SubElement(
                            sectionElement,
                            "image",
                            attrib={f"{FB2_LINK_PREFIX}:href": f"#{element.uid}"},
                        )
                    case Paragraph():
                        p = ET.Element("p")
                        self._paragraph_to_fb2(element, p)
                        sectionElement.append(p)
                    case EmptyLine():
                        ET.SubElement(sectionElement, "empty-line")
                    case ET.Element():
                        sectionElement.append(element)
        elif isinstance(chapter, ChapterWithSubchapters):
            for subchapter in chapter.subchapters:
                sectionElement.append(self._BuildSectionFromChapter(subchapter))
        else:
            raise ValueError(
                "Wrong chapter structure: second element of chapter tuple must be list!"
            )

        return sectionElement

    def _paragraph_to_fb2(self, content: ParagraphBase, parent: ET.Element) -> None:
        if isinstance(content.text, str):
            content.text = [content.text]
        for part in content.text:
            match part:
                case str():
                    if len(parent) == 0:
                        parent.text = part
                    else:
                        parent[-1].tail = part
                case named_tag:
                    child = ET.Element(named_tag.__class__.__name__.lower())
                    self._paragraph_to_fb2(part, child)
                    parent.append(child)

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
        for image in self.images:
            self._AddBinary(root, image.uid, image.media_type, image.content)

    def _AddBinary(
        self, root: ET.Element, id: str, contentType: str, data: bytes
    ) -> None:
        ET.SubElement(
            root, "binary", {"id": id, "content-type": contentType}
        ).text = b64encode(data).decode("utf-8")

    @staticmethod
    def PrettifyXml(element: ET.Element) -> str:
        dom = minidom.parseString(ET.tostring(element, "unicode"))
        return dom.toprettyxml(encoding="utf-8").decode("utf-8")
