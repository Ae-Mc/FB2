import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Sequence

from iso639 import is_language

from FB2.Author import Author
from FB2.builders.BuildAuthorName import BuildAuthorName
from FB2.constants import FB2_LINK_PREFIX
from FB2.Image import Image
from FB2.TitleInfo import TitleInfo


class TitleInfoBuilder:
    result: ET.Element

    def __init__(
        self,
        rootTag: str = "title-info",
        titleInfo: TitleInfo | None = None,
    ) -> None:
        """Calls reset() method and, if titleInfo is set, adds all fields of
        titleInfo, except coverPageImages.

        Args:
            rootTag: tag name which will be used as name of root tag.
            titleInfo: class TitleInfo object, which will be converted to
                       FB2 title-info tag.
        """

        self.reset(rootTag)
        if titleInfo:
            self.AddGenres(titleInfo.genres)
            self.AddAuthors(titleInfo.authors)
            self.AddBookTitle(titleInfo.title)
            self.AddAnnotation(titleInfo.annotation)
            self.AddKeywords(titleInfo.keywords)
            self.AddDate(titleInfo.date)
            self.AddLang(titleInfo.lang)
            self.AddSrcLang(titleInfo.srcLang)
            self.AddTranslators(titleInfo.translators)
            self.AddSequences(titleInfo.sequences)
            self.AddCoverImages(titleInfo.coverPageImages)

    def AddBookTitle(self, title: str):
        ET.SubElement(self.result, "book-title").text = title

    def AddGenres(self, genres: Sequence[str]) -> None:
        for genre in genres:
            ET.SubElement(self.result, "genre").text = genre

    def AddAuthors(self, authors: Sequence[Author | str | ET.Element]) -> None:
        for author in authors:
            if isinstance(author, ET.Element):
                self.result.append(author)
            else:
                self.result.append(BuildAuthorName("author", author))

    def AddAnnotation(self, annotation: str | Sequence[ET.Element] | None) -> None:
        if annotation is None:
            return
        annotationElement = ET.Element("annotation")
        if isinstance(annotation, str):
            for paragraph in annotation.split("\n"):
                ET.SubElement(annotationElement, "p").text = paragraph
        else:
            for element in annotation:
                annotationElement.append(element)
        self.result.append(annotationElement)

    def AddKeywords(self, keywords: Sequence[str] | None) -> None:
        if keywords:
            ET.SubElement(self.result, "keywords").text = ", ".join(keywords)

    def AddDate(self, date: tuple[datetime, str | None] | None) -> None:
        if date is not None:
            ET.SubElement(
                parent=self.result,
                tag="date",
                attrib={"value": date[0].strftime("%Y-%m-%d")},
            ).text = date[1] or date[0].strftime("%d.%m.%Y")

    def AddLang(self, lang: str) -> None:
        if not is_language(lang, ("pt1", "pt2b", "pt2t", "pt3", "pt5")):
            raise ValueError(f"Unknown language {lang}")
        ET.SubElement(self.result, "lang").text = lang

    def AddSrcLang(self, srcLang: str | None) -> None:
        if srcLang is None:
            return
        if not is_language(srcLang, ("pt1", "pt2b", "pt2t", "pt3", "pt5")):
            raise ValueError(f"Unknown language {srcLang}")
        ET.SubElement(self.result, "src-lang").text = srcLang

    def AddTranslators(
        self,
        translators: Sequence[str | ET.Element | Author] | None,
    ) -> None:
        if translators is None:
            return
        for translator in translators:
            if isinstance(translator, ET.Element):
                self.result.append(translator)
            else:
                self.result.append(BuildAuthorName("translator", translator))

    def AddSequences(
        self,
        sequences: Sequence[tuple[str, int] | ET.Element] | None,
    ) -> None:
        if sequences is None:
            return
        for sequence in sequences:
            if isinstance(sequence, ET.Element):
                self.result.append(sequence)
            else:
                ET.SubElement(
                    self.result,
                    "sequence",
                    attrib={"name": sequence[0], "number": str(sequence[1])},
                )

    def AddCoverImages(self, images: Sequence[Image] | None) -> None:
        if images is None:
            return
        coverPageElement = ET.Element("coverpage")
        for i, image in enumerate(images):
            ET.SubElement(
                coverPageElement,
                "image",
                attrib={
                    f"{FB2_LINK_PREFIX}:href": f"#{image.uid}",
                    "alt": f"Cover image {i}",
                },
            )
        self.result.append(coverPageElement)

    def GetResult(self) -> ET.Element:
        return self.result

    def reset(self, rootTag: str = "title-info") -> None:
        self.result = ET.Element(rootTag)
