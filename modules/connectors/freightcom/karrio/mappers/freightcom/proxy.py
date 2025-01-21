"""Karrio Freightcom client proxy."""

import time
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.freightcom.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings
    MAX_RETRIES = 10
    POLL_INTERVAL = 2  # seconds

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # Step 1: Submit rate request and get quote ID
        response = lib.request(
            url=f"{self.settings.server_url}/rate",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"{self.settings.api_key}",
            },
        )

        res = lib.Deserializable(response, lib.to_dict)
        rate_id = res.deserialize().get('request_id')
        if not rate_id:
            return res

        # Step 2: Poll for rate results
        for _ in range(self.MAX_RETRIES):
            quote_response = lib.request(
                url=f"{self.settings.server_url}/rate/{rate_id}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"{self.settings.api_key}",
                },
            )
            status_res = lib.Deserializable(quote_response, lib.to_dict)

            status = status_res.deserialize().get('status', {}).get('done', False)

            if status:  # Quote is complete
                return status_res

            time.sleep(self.POLL_INTERVAL)

        # If we exceed max retries
        return lib.Deserializable({
            'error': 'Rate calculation timed out'
        }, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v2/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        tracking_id = request.serialize()["tracking_id"]
        response = lib.request(
            url=f"{self.settings.server_url}/v2/track/{tracking_id}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        tracking_id = request.serialize()["tracking_id"]
        response = lib.request(
            url=f"{self.settings.server_url}/v2/track/{tracking_id}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
