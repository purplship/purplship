from attr import s
from typing import Optional


@s(auto_attribs=True)
class Error:
    error: Optional[str] = None
