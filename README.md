# FB2

[![PyPI](https://img.shields.io/pypi/v/fb2?color=orange)](https://pypi.org/project/fb2)

Python package for working with FictionBook2

## Usage example

```python
from FB2 import FictionBook2, Author
from urllib import request


book = FictionBook2()
book.titleInfo.title = "Example book"
book.titleInfo.annotation = "Small test book. Shows basics of FB2 library"
book.titleInfo.authors = [Author(firstName="Alex",
                                    middleName="Unknown",
                                    nickname="Ae_Mc",
                                    emails=["ae_mc@mail.ru"],
                                    homePages=["ae-mc.ru"])]
book.titleInfo.genres = ["sf", "sf_fantasy", "shortstory"]
book.titleInfo.coverPageImages = [
    request.urlopen("https://picsum.photos/1080/1920").read()]
book.titleInfo.sequences = [("Example books", 2)]
book.documentInfo.authors = ["Ae Mc"]
book.documentInfo.version = "1.1"
book.chapters = [
    ("Introduction", [
        "Introduction chapter first paragraph",
        "Introduction chapter second paragraph"]),
    ("1. Chapter one. FB2 format history", [
        "Introduction chapter first paragraph",
        "Introduction chapter second paragraph"])]
book.chapters.append(("2. Chapter two. Empty", []))
book.write("ExampleBook.fb2")
```

## Requirements

- iso-639 package

## Installation

- From pip: `pip install fb2`
