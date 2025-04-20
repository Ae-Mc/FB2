from urllib import request

from FB2 import Author, FictionBook2, Image

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
    request.urlopen("https://picsum.photos/1080/1920").read()
]
book.titleInfo.sequences = [("Example books", 2)]
book.documentInfo.authors = ["Ae Mc"]
book.documentInfo.version = "1.1"
book.chapters = [
    (
        "Introduction",
        [
            "Introduction chapter first paragraph",
            "Introduction chapter second paragraph",
        ],
    ),
    (
        "1. Chapter one. FB2 format history",
        [
            "Introduction chapter first paragraph",
            "Introduction chapter second paragraph",
            Image(
                media_type="image/jpeg",
                content=request.urlopen("https://picsum.photos/1920/1080").read(),
            ),
            "Text after image 1",
            "Text after image 2",
        ],
    ),
]
book.chapters.append(("2. Chapter two. Empty", []))
book.write("ExampleBook.fb2")
