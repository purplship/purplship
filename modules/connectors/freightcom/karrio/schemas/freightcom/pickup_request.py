from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DateType:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


@s(auto_attribs=True)
class ReadyType:
    hour: Optional[int] = None
    minute: Optional[int] = None


@s(auto_attribs=True)
class DispatchDetailsType:
    date: Optional[DateType] = JStruct[DateType]
    ready_at: Optional[ReadyType] = JStruct[ReadyType]
    ready_until: Optional[ReadyType] = JStruct[ReadyType]


@s(auto_attribs=True)
class ContactPhoneNumberType:
    number: Optional[str] = None
    extension: Optional[int] = None


@s(auto_attribs=True)
class PickupDetailsType:
    pre_scheduled_pickup: Optional[bool] = None
    date: Optional[DateType] = JStruct[DateType]
    ready_at: Optional[ReadyType] = JStruct[ReadyType]
    ready_until: Optional[ReadyType] = JStruct[ReadyType]
    pickup_location: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone_number: Optional[ContactPhoneNumberType] = JStruct[ContactPhoneNumberType]


@s(auto_attribs=True)
class PickupRequestType:
    pickup_details: Optional[PickupDetailsType] = JStruct[PickupDetailsType]
    dispatch_details: Optional[DispatchDetailsType] = JStruct[DispatchDetailsType]
