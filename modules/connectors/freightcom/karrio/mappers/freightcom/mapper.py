from typing import List, Tuple
from karrio.api.mapper import Mapper as BaseMapper
from karrio.mappers.freightcom.settings import Settings
from karrio.core.utils.serializable import Deserializable, Serializable
from karrio.core.models import (
    RateRequest,
    ShipmentRequest,
    ShipmentDetails,
    RateDetails,
    Message,
    ShipmentCancelRequest,
    ConfirmationDetails,
)
from karrio.providers.freightcom import (
    parse_rate_response,
    rate_request,
    parse_shipping_reply,
    shipping_request,
    shipment_cancel_request,
    parse_shipment_cancel_reply,
)


class Mapper(BaseMapper):
    settings: Settings

    # Request Mappers

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        return rate_request(payload, self.settings)

    def create_shipment_request(self, payload: ShipmentRequest) -> Serializable:
        return shipping_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: ShipmentCancelRequest
    ) -> Serializable:
        return shipment_cancel_request(payload, self.settings)

    # Response Parsers

    def parse_rate_response(
        self, response: Deserializable
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipping_reply(response, self.settings)

    def parse_cancel_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_shipment_cancel_reply(response, self.settings)
