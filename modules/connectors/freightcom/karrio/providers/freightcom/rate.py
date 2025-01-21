import karrio.schemas.freightcom.rate_request as freightcom
import karrio.schemas.freightcom.rate_response as rating
import typing
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.freightcom.error as error
import karrio.providers.freightcom.utils as provider_utils
import karrio.providers.freightcom.units as provider_units


def parse_rate_response(
    response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse Freightcom rate response into Karrio format"""
    parsed_response = response.deserialize()
    messages = error.parse_error_response(parsed_response, settings)
    rates = [_extract_details(rate, settings) for rate in parsed_response.get("rates", [])]
    return rates, messages

def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.RateType, data)

    service = provider_units.ShippingService.map(
        rate.service_id,
    )
    courier = provider_units.ShippingCourier.find(rate.service_id)

    charges = [
        ("Base charge", rate.base.value, rate.base.currency),
        *((surcharge.type, surcharge.amount.value, surcharge.amount.currency) for surcharge in rate.surcharges),
        *((tax.type, tax.amount.value, tax.amount.currency) for tax in rate.taxes),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(int(rate.total.value) / 100),
        currency=rate.total.currency,
        transit_days=lib.to_int(rate.transit_time_days),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                currency=currency,
                amount=lib.to_money(int(amount) / 100),
            )
            for name, amount, currency in charges
            if charges
        ],
        meta=dict(
            rate_provider=courier.name,
            service_name=service.name ,
        ),
    )

def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a Freightcom rate request from Karrio unified request"""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )

    packaging_type = provider_units.PackagingType.map(packages.package_type or "small_box").value
    ship_datetime = lib.to_next_business_datetime(
        options.shipping_date.state or datetime.datetime.now(),
        current_format="%Y-%m-%dT%H:%M",
    )

    request = freightcom.RateRequestType(
        services=payload.services or [],
        excluded_services=[],
        details=freightcom.DetailsType(
            origin=freightcom.DestinationType(
                name=shipper.company_name or shipper.person_name,
                address=freightcom.AddressType(
                    address_line_1=shipper.address_line1,
                    address_line_2=shipper.address_line2,
                    city=shipper.city,
                    region=shipper.state_code,
                    country=shipper.country_code,
                    postal_code=shipper.postal_code,
                ),
                residential=shipper.residential,
                contact_name=shipper.person_name if shipper.company_name else "",
                phone_number=freightcom.PhoneNumberType(
                    number=shipper.phone_number
                ) if shipper.phone_number else None,
                email_addresses=lib.join(shipper.email),
            ),
            destination=freightcom.DestinationType(
                name=recipient.company_name or recipient.person_name,
                address=freightcom.AddressType(
                    address_line_1=recipient.address_line1,
                    address_line_2=recipient.address_line2,
                    city=recipient.city,
                    region=recipient.state_code,
                    country=recipient.country_code,
                    postal_code=recipient.postal_code,
                ),
                residential=recipient.residential,
                contact_name=recipient.person_name,
                phone_number=freightcom.PhoneNumberType(
                    number=recipient.phone_number
                ) if recipient.phone_number else None,
                email_addresses=lib.join(recipient.email),
                ready_at=freightcom.ReadyType(
                    hour=ship_datetime.hour,
                    minute=0
                ),
                ready_until=freightcom.ReadyType(
                    hour=17,
                    minute=0
                ),
                signature_requirement="required" if options.signature_confirmation.state else "not-required"
            ),
            expected_ship_date=freightcom.ExpectedShipDateType(
                year=ship_datetime.year,
                month=ship_datetime.month,
                day=ship_datetime.day,
            ),
            packaging_type=packaging_type,
            packaging_properties=(
                freightcom.PackagingPropertiesType(
                pallet_type="ltl" if packaging_type == "pallet" else None,
                has_stackable_pallets=options.stackable.state if packaging_type == "pallet" else None,
                dangerous_goods=options.dangerous_goods.state,
                dangerous_goods_details=freightcom.DangerousGoodsDetailsType(
                    packaging_group=options.dangerous_goods_group.state,
                    goods_class=options.dangerous_goods_class.state,
                ) if options.dangerous_goods.state else None,
                pallets=[
                    freightcom.PalletType(
                        measurements=freightcom.PalletMeasurementsType(
                            weight=freightcom.WeightType(
                                unit="kg" if parcel.weight_unit.upper() == "KG" else "lb",
                                value=lib.to_decimal(parcel.weight)
                            ),
                            cuboid=freightcom.CuboidType(
                                unit="cm" if parcel.dimension_unit.upper() == "CM" else "in",
                                l=lib.to_int(parcel.length),
                                w=lib.to_int(parcel.width),
                                h=lib.to_int(parcel.height)
                            )
                        ),
                        description=parcel.description,
                        freight_class=options.freight_class.state,
                    ) for parcel in payload.parcels
                ] if packaging_type == "pallet" else [],
                packages=[
                    freightcom.PackageType(
                        measurements=freightcom.PackageMeasurementsType(
                            weight=freightcom.WeightType(
                                unit="kg" if parcel.weight_unit.upper() == "KG" else "lb",
                                value=lib.to_decimal(parcel.weight)
                            ),
                            cuboid=freightcom.CuboidType(
                                unit="cm" if parcel.dimension_unit.upper() == "CM" else "in",
                                l=lib.to_int(parcel.length),
                                w=lib.to_int(parcel.width),
                                h=lib.to_int(parcel.height)
                            )
                        ),
                        description=parcel.description,
                    ) for parcel in payload.parcels
                ] if packaging_type == "package" else [],
                    courierpaks=[
                    freightcom.CourierpakType(
                        measurements=freightcom.CourierpakMeasurementsType(
                            weight=freightcom.WeightType(
                                unit="kg" if parcel.weight_unit.upper() == "KG" else "lb",
                                value=lib.to_decimal(parcel.weight)
                            )
                        ),
                        description=parcel.description,
                    ) for parcel in payload.parcels
                ] if packaging_type == "courier-pak" else [],
                insurance=freightcom.InsuranceType(
                    type='carrier',
                    total_cost=freightcom.TotalCostType(
                        currency=options.currency.state or "CAD",
                        value=lib.to_int(options.insurance.state)
                    )
                ) if options.insurance.state else None,
                pallet_service_details=freightcom.PalletServiceDetailsType() if packaging_type == "pallet" else None,
            )

            ),
            reference_codes=[payload.reference] if payload.reference else []
        )
    )

    return lib.Serializable(request, lib.to_dict)


