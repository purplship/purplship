import typing
import pathlib
import karrio.lib as lib
import karrio.core.units as units

METADATA_JSON = lib.load_json(pathlib.Path(__file__).resolve().parent / "metadata.json")

FREIGHTCOM_CARRIER_METADATA = [_ for _ in METADATA_JSON["PROD_SERVICES"] + METADATA_JSON["DEV_SERVICES"]]



KARRIO_CARRIER_MAPPING = {
    "Freightcom": "freightcom",
    "ups_courier": "ups",
    "canada_post": "canadapost",
    'fed_ex_courier': "fedex",
    'fed_ex_express': "fedex",
    'fed_ex_freight': "fedex",
    'fed_ex_ground': "fedex",
    "dhl_canada": "dhl_express",
    "dhl_e_commerce": "dhl_express",
}


class PackagingType(lib.StrEnum):
    # TODO: review types
    freightcom_pallet = "pallet"
    freightcom_drum = "Drum"
    freightcom_boxes = "Boxes"
    freightcom_rolls = "Rolls"
    freightcom_pipes_tubes = "Pipes/Tubes"
    freightcom_bales = "Bales"
    freightcom_bags = "Bags"
    freightcom_cylinder = "Cylinder"
    freightcom_pails = "Pails"
    freightcom_reels = "Reels"

    freightcom_envelope = "envelope"
    freightcom_courier = "courier-pak"
    freightcom_pak = "courier-pak"
    freightcom_package = "package"

    """ Unified Packaging type mapping """
    envelope = freightcom_envelope
    pak = freightcom_pak
    tube = freightcom_pipes_tubes
    pallet = freightcom_pallet
    small_box = freightcom_package
    medium_box = freightcom_package
    your_packaging = freightcom_package


class PaymentMethodType(lib.StrEnum):
    net_terms = "net-terms"
    credit_card = "credit-card"

class PaymentType(lib.StrEnum):  # TODO:: retrieve the complete list of payment types
    sender = "shipper"
    recipient = "receiver"
    third_party = "other"

class CustomsContentType(lib.StrEnum):
    sale = "commercially-sold-goods"
    gift = "gift"
    sample = "commercial-sample"
    repair = "repair-warranty"
    return_merchandise = "return-shipment"
    other = "other"

    """ Unified Content type mapping """
    documents = other
    merchandise = sale

# class PaymentMethodID(lib.StrEnum):
#     ""

class ShippingOption(lib.Enum):
    freightcom_signature_required =  lib.OptionEnum("signatureRequired", bool)
    freightcom_saturday_pickup_required = lib.OptionEnum("saturdayPickupRequired", bool)
    freightcom_homeland_security = lib.OptionEnum("homelandSecurity", bool)
    freightcom_exhibition_convention_site = lib.OptionEnum(
        "exhibitionConventionSite", bool
    )
    freightcom_military_base_delivery = lib.OptionEnum("militaryBaseDelivery", bool)
    freightcom_customs_in_bond_freight = lib.OptionEnum("customsIn_bondFreight", bool)
    freightcom_limited_access = lib.OptionEnum("limitedAccess", bool)
    freightcom_excess_length = lib.OptionEnum("excessLength", bool)
    freightcom_tailgate_pickup = lib.OptionEnum("tailgatePickup", bool)
    freightcom_residential_pickup = lib.OptionEnum("residentialPickup", bool)
    freightcom_cross_border_fee = lib.OptionEnum("crossBorderFee", bool)
    freightcom_notify_recipient = lib.OptionEnum("notifyRecipient", bool)
    freightcom_single_shipment = lib.OptionEnum("singleShipment", bool)
    freightcom_tailgate_delivery = lib.OptionEnum("tailgateDelivery", bool)
    freightcom_residential_delivery = lib.OptionEnum("residentialDelivery", bool)
    freightcom_insurance_type = lib.OptionEnum("insuranceType", float)
    freightcom_inside_delivery = lib.OptionEnum("insideDelivery", bool)
    freightcom_is_saturday_service = lib.OptionEnum("isSaturdayService", bool)
    freightcom_dangerous_goods_type = lib.OptionEnum("dangerousGoodsType", bool)
    freightcom_stackable = lib.OptionEnum("stackable", bool)
    freightcom_payment_method = lib.OptionEnum("payment_method", str)

    """ Unified Option type mapping """
    saturday_delivery = freightcom_saturday_pickup_required
    signature_confirmation = freightcom_signature_required



def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


def to_carrier_code(service: str) -> str:
    _code = lib.to_snake_case(service['carrier_name'])
    return KARRIO_CARRIER_MAPPING.get(_code, _code)

def to_service_code(service: typing.Dict[str, str]) -> str:
    return f"freightcom_{to_carrier_code(service)}_{lib.to_slug(service['service_name'])}"

def find_courier(search: str):
    courier: dict = next(
        (
            item
            for item in FREIGHTCOM_CARRIER_METADATA
            if to_carrier_code(item) == search
            or item['carrier_name'] == search
            or item['id'] == search
        ),
        {},
    )

    if courier:
        return ShippingCourier.map(to_carrier_code(courier))

    return ShippingCourier.map(search)

def get_carrier_name(carrier_id: str) -> str:
    return next(
        (
            service['carrier_name']
            for service in METADATA_JSON["PROD_SERVICES"]
            if service['id'].split('.')[0] == carrier_id
        ),
        None
    )

# FREIGHTCOM_SERVICE_METADATA = {
#     lib.to_snake_case(service['service_name']): {
#         **service,
#         'carrier': service['id'].split('.')[0].split('-')[0],
#         'carrier_name': service['carrier_name']
#     }
#     for service in METADATA_JSON["PROD_SERVICES"] + METADATA_JSON["DEV_SERVICES"]
# }


ShippingService = lib.StrEnum(
    "ShippingService",
    {
        to_service_code(service): service['id']
        for service in FREIGHTCOM_CARRIER_METADATA
    },
)
ShippingCourier = lib.StrEnum(
    "ShippingCourier",
    {
        to_carrier_code(service): service['carrier_name']
        for service in FREIGHTCOM_CARRIER_METADATA
    },
)
# RateProvider = lib.StrEnum(
#     "RateProvider",
#     {
#         carrier_id: carrier['name']
#         for carrier_id, carrier in FREIGHTCOM_CARRIER_METADATA.items()
#     },
# )


setattr(ShippingCourier, "find", find_courier)

