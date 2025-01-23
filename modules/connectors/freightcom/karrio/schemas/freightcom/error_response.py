from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DataType:
    services: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    message: Optional[str] = None
    data: Optional[DataType] = JStruct[DataType]
