import typing
import karrio.lib as lib
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
        # *sum(
        #     [
        #         [dict(code="warning", message=__) for __ in _.get("warnings")]
        #         for _ in responses
        #         if _.get("warnings")
        #     ],
        #     [],
        # ),
        # *sum(
        #     [
        #         [
        #             dict(
        #                 code="error",
        #                 message=order["message"]
        #             )
        #             for order in _.get("order", [])
        #             if "message" in order and order["message"].startswith("Error")
        #         ]
        #         for _ in responses
        #     ],
        #     [],
        # )
    ]
    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details={
                **kwargs,
                "type": error.get("type"),
                "fieldErrors": error.get("fieldErrors"),
                "thirdPartyMessage": error.get("thirdPartyMessage"),
            },
        )
        for error in errors
    ]


