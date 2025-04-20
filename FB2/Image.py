from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Image:
    """Image object

    Attributes:
        uid: unique image identifier (recommended to use default — it will use uuid4)
        content: image content in bytes
        media_type: image media type, like image/jpeg
    """

    media_type: str
    content: bytes
    uid: str = field(default_factory=lambda: uuid4().hex)
