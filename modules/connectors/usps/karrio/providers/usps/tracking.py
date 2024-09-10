"""Karrio USPS rating API implementation."""

# import karrio.schemas.usps.tracking_request as usps
import karrio.schemas.usps.tracking_response as tracking

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.usps.error as error
import karrio.providers.usps.utils as provider_utils
import karrio.providers.usps.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(details, settings)
        for _, details in responses
        if "error" not in details
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(tracking.TrackingResponseType, data)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(details, "status", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.trackingNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventTimestamp, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.name,
                code=event.eventType,
                time=lib.flocaltime(event.eventTimestamp, "%Y-%m-%dT%H:%M:%SZ"),
                location=lib.text(
                    event.eventCity,
                    event.eventZIP,
                    event.eventState,
                    event.eventCountry,
                    separator=", ",
                ),
            )
            for event in details.trackingEvents
        ],
        estimated_delivery=lib.fdate(
            details.expectedDeliveryTimeStamp,
            "%Y-%m-%dT%H:%M:%SZ",
        ),
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            # fmt: off
            carrier_tracking_link=settings.tracking_url.format(details.trackingNumber),
            expected_delivery=lib.fdate(details.expectedDeliveryTimeStamp, "%Y-%m-%dT%H:%M:%SZ"),
            shipment_service=provider_units.ShippingService.map(details.serviceTypeCode).name_or_key,
            shipment_origin_country=details.originCountry,
            shipment_origin_postal_code=details.originZIP,
            shipment_destination_country=details.destinationCountryCode,
            shipment_destination_postal_code=details.destinationZIP,
            # fmt: on
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to usps specific type
    request = payload.tracking_numbers

    return lib.Serializable(request, lib.to_dict)
