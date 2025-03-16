from dataclasses import dataclass


@dataclass
class Image:
    """Image object

    Attributes:
        uid: unique image identifier
        content: image content in bytes
        media_type: image media type, like image/jpeg
    """

    uid: str
    media_type: str
    content: bytes
