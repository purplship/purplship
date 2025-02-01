from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    unit_number: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


@s(auto_attribs=True)
class PhoneNumberType:
    number: Optional[str] = None
    extension: Optional[int] = None


@s(auto_attribs=True)
class ReadyType:
    hour: Optional[int] = None
    minute: Optional[int] = None


@s(auto_attribs=True)
class DestinationType:
    name: Optional[str] = None
    address: Optional[AddressType] = JStruct[AddressType]
    residential: Optional[bool] = None
    tailgate_required: Optional[bool] = None
    instructions: Optional[str] = None
    contact_name: Optional[str] = None
    phone_number: Optional[PhoneNumberType] = JStruct[PhoneNumberType]
    email_addresses: List[str] = []
    receives_email_updates: Optional[bool] = None
    ready_at: Optional[ReadyType] = JStruct[ReadyType]
    ready_until: Optional[ReadyType] = JStruct[ReadyType]
    signature_requirement: Optional[str] = None


@s(auto_attribs=True)
class ExpectedShipDateType:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


@s(auto_attribs=True)
class WeightType:
    unit: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class CourierpakMeasurementsType:
    weight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class CourierpakType:
    measurements: Optional[CourierpakMeasurementsType] = JStruct[CourierpakMeasurementsType]
    description: Optional[str] = None


@s(auto_attribs=True)
class DangerousGoodsDetailsType:
    packaging_group: Optional[str] = None
    goods_class: Optional[str] = None
    description: Optional[str] = None
    united_nations_number: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone_number: Optional[PhoneNumberType] = JStruct[PhoneNumberType]


@s(auto_attribs=True)
class TotalCostType:
    currency: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class InsuranceType:
    type: Optional[str] = None
    total_cost: Optional[TotalCostType] = JStruct[TotalCostType]


@s(auto_attribs=True)
class CuboidType:
    unit: Optional[str] = None
    l: Optional[int] = None
    w: Optional[int] = None
    h: Optional[int] = None


@s(auto_attribs=True)
class PackageMeasurementsType:
    weight: Optional[WeightType] = JStruct[WeightType]
    cuboid: Optional[CuboidType] = JStruct[CuboidType]


@s(auto_attribs=True)
class PackageType:
    measurements: Optional[PackageMeasurementsType] = JStruct[PackageMeasurementsType]
    description: Optional[str] = None


@s(auto_attribs=True)
class InBondDetailsType:
    type: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    contact_method: Optional[str] = None
    contact_email_address: Optional[str] = None
    contact_phone_number: Optional[PhoneNumberType] = JStruct[PhoneNumberType]


@s(auto_attribs=True)
class PalletServiceDetailsType:
    limited_access_delivery_type: Optional[str] = None
    limited_access_delivery_other_name: Optional[str] = None
    in_bond: Optional[bool] = None
    in_bond_details: Optional[InBondDetailsType] = JStruct[InBondDetailsType]
    appointment_delivery: Optional[bool] = None
    protect_from_freeze: Optional[bool] = None
    threshold_pickup: Optional[bool] = None
    threshold_delivery: Optional[bool] = None


@s(auto_attribs=True)
class PalletType:
    measurements: Optional[PackageMeasurementsType] = JStruct[PackageMeasurementsType]
    description: Optional[str] = None
    freight_class: Optional[str] = None
    nmfc: Optional[str] = None
    contents_type: Optional[str] = None
    num_pieces: Optional[int] = None


@s(auto_attribs=True)
class PackagingPropertiesType:
    pallet_type: Optional[str] = None
    has_stackable_pallets: Optional[bool] = None
    dangerous_goods: Optional[str] = None
    dangerous_goods_details: Optional[DangerousGoodsDetailsType] = JStruct[DangerousGoodsDetailsType]
    pallets: List[PalletType] = JList[PalletType]
    packages: List[PackageType] = JList[PackageType]
    courierpaks: List[CourierpakType] = JList[CourierpakType]
    includes_return_label: Optional[bool] = None
    special_handling_required: Optional[bool] = None
    has_dangerous_goods: Optional[bool] = None
    pallet_service_details: Optional[PalletServiceDetailsType] = JStruct[PalletServiceDetailsType]
    insurance: Optional[InsuranceType] = JStruct[InsuranceType]


@s(auto_attribs=True)
class DetailsType:
    origin: Optional[DestinationType] = JStruct[DestinationType]
    destination: Optional[DestinationType] = JStruct[DestinationType]
    expected_ship_date: Optional[ExpectedShipDateType] = JStruct[ExpectedShipDateType]
    packaging_type: Optional[str] = None
    packaging_properties: Optional[PackagingPropertiesType] = JStruct[PackagingPropertiesType]
    reference_codes: List[str] = []


@s(auto_attribs=True)
class RateRequestType:
    services: List[str] = []
    excluded_services: List[str] = []
    details: Optional[DetailsType] = JStruct[DetailsType]
