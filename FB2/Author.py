from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Author:
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    nickname: Optional[str] = None
    homePages: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    id: Optional[str] = None
