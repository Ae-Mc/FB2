from typing import Sequence

from pydantic import BaseModel


class Author(BaseModel):
    """Holds information about author

    Attributes:
        firstName: author's first name
        middleName: author's middle name
        lastName: author's last name
        nickname: author's nickname
        homePages: list of author's websites
        emails: list of author's emails
        id: author's unique id
    """

    firstName: str | None = None
    middleName: str | None = None
    lastName: str | None = None
    nickname: str | None = None
    homePages: Sequence[str] | None = None
    emails: Sequence[str] | None = None
    id: str | None = None
