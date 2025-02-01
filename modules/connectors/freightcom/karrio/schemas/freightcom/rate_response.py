from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class BaseType:
    currency: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class SurchargeType:
    type: Optional[str] = None
    amount: Optional[BaseType] = JStruct[BaseType]


@s(auto_attribs=True)
class ValidUntilType:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


@s(auto_attribs=True)
class RateType:
    carrier_name: Optional[str] = None
    service_name: Optional[str] = None
    service_id: Optional[str] = None
    valid_until: Optional[ValidUntilType] = JStruct[ValidUntilType]
    total: Optional[BaseType] = JStruct[BaseType]
    base: Optional[BaseType] = JStruct[BaseType]
    surcharges: List[SurchargeType] = JList[SurchargeType]
    taxes: List[SurchargeType] = JList[SurchargeType]
    transit_time_days: Optional[int] = None
    transit_time_not_available: Optional[bool] = None


@s(auto_attribs=True)
class StatusType:
    done: Optional[bool] = None
    total: Optional[int] = None
    complete: Optional[int] = None


@s(auto_attribs=True)
class RateResponseType:
    status: Optional[StatusType] = JStruct[StatusType]
    rates: List[RateType] = JList[RateType]
