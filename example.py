import sys
from urllib import request

sys.path.append("./src")

from FB2 import (
    Author,
    BaseChapter,
    ChapterWithSubchapters,
    FictionBook2,
    Image,
    SimpleChapter,
)

book = FictionBook2()
book.titleInfo.title = "Example book"
book.titleInfo.annotation = "Small test book. Shows basics of FB2 library"
book.titleInfo.authors = [
    Author(
        firstName="Alex",
        middleName="Unknown",
        nickname="Ae_Mc",
        emails=["ae_mc@mail.ru"],
        homePages=["ae-mc.ru"],
    )
]
book.titleInfo.genres = ["sf", "sf_fantasy", "shortstory"]
book.titleInfo.coverPageImages = [
    Image(
        media_type="image/jpeg",
        content=request.urlopen("https://picsum.photos/1080/1920").read(),
    ),
    # Multiple cover images not supported by most FB2 readers.
    # Image(
    #     media_type="image/jpeg",
    #     content=request.urlopen("https://picsum.photos/1080/1920").read(),
    # ),
]
book.titleInfo.sequences = [("Example books", 2)]
book.documentInfo.authors = ["Ae Mc"]
book.documentInfo.version = "1.1"

book.chapters = list[BaseChapter](
    [
        SimpleChapter(
            title="Introduction",
            content=[
                "Introduction chapter first paragraph",
                "Introduction chapter second paragraph",
            ],
        ),
        SimpleChapter(
            title="1. Chapter one. FB2 format history",
            content=[
                "Introduction chapter first paragraph",
                "Introduction chapter second paragraph",
                Image(
                    media_type="image/jpeg",
                    content=request.urlopen("https://picsum.photos/1920/1080").read(),
                ),
                "Text after image 1",
                Image(
                    media_type="image/jpeg",
                    content=request.urlopen("https://picsum.photos/1920/1080").read(),
                ),
                "Text after image 2",
            ],
        ),
    ]
)

# Example of adding chapter with subchapters (subsections)
book.chapters.append(
    ChapterWithSubchapters(
        title="2. Chapter two. With subchapters (subsections)",
        epigraph=[
            "This is the epigraph for chapter two. It can be multiline.",
            "This is the second line of the epigraph.",
        ],
        annotation=[
            "This is the annotation for chapter two. It can also be multiline.",
            "This is the second line of the annotation.",
            "This chapter also contains cover image that goes before the text.",
        ],
        image=Image(
            media_type="image/jpeg",
            content=request.urlopen("https://picsum.photos/1920/1080").read(),
        ),
        subchapters=[
            SimpleChapter(
                title="Subchapter 2.1",
                content=[
                    "Subchapter 2.1 text",
                    "Subchapter 2.1 text 2",
                ],
            ),
            SimpleChapter(
                title="Subchapter 2.2",
                content=[
                    "Subchapter 2.2 text",
                    "Subchapter 2.2 text 2",
                ],
            ),
            ChapterWithSubchapters(
                title="Subchapter 2.3",
                subchapters=[
                    SimpleChapter(
                        title="Subsubchapter 2.3.1",
                        content=[
                            "Subsubchapter 2.3.1 text",
                            "Subsubchapter 2.3.1 text 2",
                        ],
                    ),
                    SimpleChapter(
                        title="Subsubchapter 2.3.2",
                        content=[
                            "Subsubchapter 2.3.2 text",
                            "Subsubchapter 2.3.2 text 2",
                        ],
                    ),
                ],
            ),
        ],
    ),
)

book.chapters.append(SimpleChapter(title="3. Chapter three. Empty"))
book.write("ExampleBook.fb2")
