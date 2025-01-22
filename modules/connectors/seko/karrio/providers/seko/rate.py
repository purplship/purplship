"""Karrio SEKO Logistics rating API implementation."""

import karrio.schemas.seko.rating_request as seko
import karrio.schemas.seko.rating_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response.get("Available", [])]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = lib.to_object(rating.AvailableType, data)
    service = provider_units.ShippingService.map(details.DeliveryType)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(details.Cost),
        currency=settings.connection_config.currency.state or "USD",
        meta=dict(
            service_name=service.value_or_key,
            seko_carrier=details.CarrierName,
            Route=details.Route,
            QuoteId=details.QuoteId,
            DeliveryType=details.DeliveryType,
            CarrierServiceType=details.CarrierServiceType,
            IsFreightForward=details.IsFreightForward,
            IsRuralDelivery=details.IsRuralDelivery,
            IsSaturdayDelivery=details.IsSaturdayDelivery,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    recipient = lib.to_address(payload.recipient)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to seko specific type
    request = seko.RatingRequestType(
        DeliveryReference=payload.reference,
        Destination=seko.DestinationType(
            Id=options.seko_destination_id.state,
            Name=recipient.company_name,
            Address=seko.AddressType(
                BuildingName="",
                StreetAddress=recipient.street,
                Suburb=recipient.city,
                City=recipient.state_code,
                PostCode=recipient.postal_code,
                CountryCode=recipient.country_code,
            ),
            ContactPerson=recipient.contact,
            PhoneNumber=recipient.phone_number,
            Email=recipient.email,
            DeliveryInstructions=options.destination_instructions.state,
            RecipientTaxId=recipient.tax_id,
        ),
        IsSaturdayDelivery=options.seko_is_saturday_delivery.state,
        IsSignatureRequired=options.seko_is_signature_required.state,
        Packages=[
            seko.PackageType(
                Height=package.height.CM,
                Length=package.length.CM,
                Id=package.options.seko_package_id.state,
                Width=package.width.CM,
                Kg=package.weight.KG,
                Name=lib.text(package.description, max=50),
                Type=provider_units.PackagingType.map(
                    package.packaging_type or "your_packaging"
                ).value,
            )
            for package in packages
        ],
    )

    return lib.Serializable(request, lib.to_dict)
