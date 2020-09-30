import xml.etree.ElementTree as ET
from typing import List, Union, Tuple
from datetime import datetime
from .BuildAuthorName import BuildAuthorName


class FB2TitileInfoBuilder:
    result: ET.Element

    def __init__(self):
        self.reset()

    def AddGenres(self, genres: List[str]) -> None:
        for genre in genres:
            ET.SubElement(self.result, "genre").text = genre

    def AddAuthors(self, authors: List[Union[str, ET.Element]]) -> None:
        for author in authors:
            if isinstance(author, str):
                self.result.append(BuildAuthorName("author", author))
            else:
                self.result.append(author)

    def AddAnnotation(self, annotation: Union[str, List[ET.Element]]) -> None:
        annotationElement = ET.Element("annotation")
        if isinstance(annotation, str):
            for paragraph in annotation.split('\n'):
                ET.SubElement(annotationElement, "p").text = paragraph
        else:
            for element in annotation:
                annotationElement.append(element)
        self.result.append(annotationElement)

    def AddKeywords(self, keywords: List[str]) -> None:
        ET.SubElement(self.result, "keywords").text = "\n".join(keywords)

    def AddDate(self, date: datetime, dateText: str = None) -> None:
        dateElement = ET.Element("date")
        dateElement.attrib["value"] = date.strftime("%Y-%m-%d")
        dateElement.text = dateText or date.strftime("%d.%m.%Y")
        self.result.append(dateElement)

    def AddLang(self, lang: str) -> None:
        ET.SubElement(self.result, "lang").text = lang

    def AddSrcLang(self, srcLang: str) -> None:
        ET.SubElement(self.result, "src-lang").text = srcLang

    def AddTranslators(self,
                       translators: List[Union[str, ET.Element]]) -> None:
        for translator in translators:
            if isinstance(translator, str):
                self.result.append(BuildAuthorName("translator", translator))
            else:
                self.result.append(translator)

    def AddSequences(
            self, sequences: List[Union[Tuple[str, int], ET.Element]]) -> None:
        for sequence in sequences:
            if isinstance(sequence, ET.Element):
                self.result.append(sequence)
            else:
                ET.SubElement(self.result, "sequence", attrib={
                    "name": sequence[0],
                    "number": str(sequence[1])
                })

    def AddCoverImages(self, coverLinks: List[str]) -> None:
        coverPageElement = ET.Element("coverpage")
        for coverLink in coverLinks:
            ET.SubElement(coverPageElement, "image", attrib={
                "xlink:href": coverLink,
                "alt": "Cover image"
            })
        self.result.append(coverPageElement)

    def GetResult(self) -> ET.Element:
        return self.result

    def reset(self) -> None:
        self.result = ET.Element("title-info")
