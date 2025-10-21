from uuid import uuid4

from pydantic import BaseModel, Field


class Image(BaseModel):
    """Image object

    Attributes:
        uid: unique image identifier (recommended to use default — it will use uuid4)
        content: image content in bytes
        media_type: image media type, like image/jpeg
    """

    media_type: str
    content: bytes
    uid: str = Field(default_factory=lambda: uuid4().hex)
