from typing import Sequence

from pydantic import BaseModel


class EmptyLine(BaseModel):
    pass


class ParagraphBase(BaseModel):
    text: (
        "str | Sequence[str | Strong | Emphasis | A | Strikethrough | Sub | Sup | Code]"
    )


class Paragraph(ParagraphBase):
    pass


class Strong(ParagraphBase):
    pass


class Emphasis(ParagraphBase):
    pass


class A(ParagraphBase):
    pass


class Strikethrough(ParagraphBase):
    pass


class Sub(ParagraphBase):
    pass


class Sup(ParagraphBase):
    pass


class Code(ParagraphBase):
    pass
