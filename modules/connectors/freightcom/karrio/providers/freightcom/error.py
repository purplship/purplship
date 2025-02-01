import typing
import karrio.core.models as models
import karrio.providers.freightcom.utils as provider_utils

def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]

    errors = [
        *[_ for _ in responses if _.get("message")],
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            message=error.get("message"),
            details={
                **kwargs,
                **(error.get('data', {}))
            },
        )
        for error in errors
    ]


