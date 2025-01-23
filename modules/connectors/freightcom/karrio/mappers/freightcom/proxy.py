"""Karrio Freightcom client proxy."""

import time
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.freightcom.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings
    MAX_RETRIES = 10
    POLL_INTERVAL = 2  # seconds

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        # Step 1: Submit rate request and get quote ID
        response = self._send_request(
            path="/rate", request=lib.Serializable(request.value, lib.to_json)
        )

        rate_id = lib.to_dict(response).get('request_id')
        if not rate_id:
            return lib.Deserializable(response, lib.to_dict)

        # Step 2: Poll for rate results
        for _ in range(self.MAX_RETRIES):
            status_res = self._send_request(
                path=f"/rate/{rate_id}",
                method="GET"
            )

            status = lib.to_dict(status_res).get('status', {}).get('done', False)

            if status:  # Quote is complete
                return lib.Deserializable(status_res, lib.to_dict)

            time.sleep(self.POLL_INTERVAL)

        # If we exceed max retries
        return lib.Deserializable({
            'message': 'Rate calculation timed out'
        }, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:

        response = self._send_request(
                path="/shipment", request=lib.Serializable(request.value, lib.to_json)
            )

        shipment_id = lib.to_dict(response).get('id')
        if not shipment_id:
            return lib.Deserializable(response, lib.to_dict)


        # Step 2: retry because api return empty bytes if done to fast
        time.sleep(1)
        for _ in range(self.MAX_RETRIES):

            shipment_response = self._send_request(path=f"/shipment/{shipment_id}", method="GET")
            shipment_res = lib.failsafe(lambda :lib.to_dict(shipment_response)) or lib.decode(shipment_response)

            if shipment_res:  # is complete
                return lib.Deserializable(shipment_res, lib.to_dict, request.ctx)

            time.sleep(self.POLL_INTERVAL)

        # If we exceed max retries
        return lib.Deserializable({
            'message': 'timed out'
        }, lib.to_dict)


    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(path=f"/shipment/{request.serialize()}/tracking-events")

        return lib.Deserializable(response, lib.to_dict)

    # TODO: not sure how this can be a dynamic unit Enum, and cached for now i hard code the id in the ship request
    def get_payments_methods(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(
            path="/finance/payment-methods",
            method="GET"
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path=f"/shipment/{request.serialize()}", method="DELETE"
        )
        return lib.Deserializable(response if any(response) else "{}", lib.to_dict)

    def _send_request(
        self, path: str, request: lib.Serializable = None, method: str = "POST"
    ) -> str:

        data: dict = dict(data=request.serialize()) if request is not None else dict()
        return lib.request(
            **{
                "url": f"{self.settings.server_url}{path}",
                "trace": self.trace_as("json"),
                "method": method,
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": self.settings.api_key,
                },
                **data,
            }
        )
