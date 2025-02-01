from typing import List, Tuple
from karrio.api.mapper import Mapper as BaseMapper
from karrio.mappers.freightcom.settings import Settings
from karrio.core.utils.serializable import Deserializable, Serializable
import karrio.core.models as models
import karrio.providers.freightcom as provider


class Mapper(BaseMapper):
    settings: Settings

    # Request Mappers

    def create_rate_request(self, payload: models.RateRequest) -> Serializable:
        return provider.rate_request(payload, self.settings)

    def create_shipment_request(self, payload: models.ShipmentRequest) -> Serializable:
        return provider.create_shipment_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> Serializable:
        return provider.shipment_cancel_request(payload, self.settings)

    # Response Parsers

    def parse_rate_response(
        self, response: Deserializable
    ) -> Tuple[List[models.RateDetails], List[models.Message]]:
        return provider.parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: Deserializable
    ) -> Tuple[models.ShipmentDetails, List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)

    def parse_cancel_shipment_response(
        self, response: Deserializable
    ) -> Tuple[models.ConfirmationDetails, List[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)
