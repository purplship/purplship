import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.freightcom.error as error
import karrio.providers.freightcom.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = not any(messages)

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def shipment_cancel_request(payload: models.ShipmentCancelRequest, _) -> lib.Serializable:
    return lib.Serializable(payload.shipment_identifier)
