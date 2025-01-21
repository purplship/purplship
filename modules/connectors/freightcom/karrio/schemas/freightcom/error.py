from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DataType:
    details_destination_signature_requirement: Optional[str] = None


@s(auto_attribs=True)
class ErrorType:
    message: Optional[str] = None
    data: Optional[DataType] = JStruct[DataType]
