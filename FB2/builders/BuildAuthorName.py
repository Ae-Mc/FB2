import xml.etree.ElementTree as ET


def BuildAuthorName(rootTag: str, name: str) -> ET.Element:
    rootElement = ET.Element(rootTag)
    authorNameParts = name.split(' ')
    if len(authorNameParts) == 1:
        ET.SubElement(rootElement, "nickname").text = authorNameParts[0]
    elif len(authorNameParts) == 2:
        ET.SubElement(rootElement, "first-name").text = authorNameParts[0]
        ET.SubElement(rootElement, "last-name").text = authorNameParts[1]
    elif len(authorNameParts) == 3:
        ET.SubElement(rootElement, "first-name").text = authorNameParts[0]
        ET.SubElement(rootElement, "last-name").text = authorNameParts[1]
        ET.SubElement(rootElement, "middle-name").text = authorNameParts[2]
    return rootElement
