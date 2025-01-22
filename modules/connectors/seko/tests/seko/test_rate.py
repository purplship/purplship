import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ratesqueryv1/availablerates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "address_line1": "DestinationStreetAddress",
        "city": "Christchurch",
        "postal_code": "8061",
        "country_code": "NZ",
        "person_name": "DestinationName",
        "phone_number": "123456789",
        "email": "destinationemail@email.com",
        "state_tax_id": "123456",
    },
    "parcels": [
        {
            "height": 1,
            "length": 1,
            "weight": 0.1,
            "width": 10,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "description": "SATCHEL",
            "packaging_type": "small_box",
        }
    ],
    "options": {
        "saturday_delivery": False,
        "seko_is_signature_required": True,
        "destination_instructions": "Desinationdeliveryinstructions",
    },
    "reference": "ORDER123",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "currency": "GBP",
            "meta": {
                "CarrierServiceType": "InternationalCourier",
                "DeliveryType": "AIR TRACKED",
                "IsFreightForward": False,
                "IsRuralDelivery": False,
                "IsSaturdayDelivery": False,
                "QuoteId": "e7fdf36c-8f6a-4d3f-8d96-c8b5893a0e7f",
                "Route": "OFFSHORE->AKL- SI",
                "seko_carrier": "Omni Parcel",
                "service_name": "AIR TRACKED",
            },
            "service": "AIR TRACKED",
            "total_charge": 5.82,
        }
    ],
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "code": "ValidationError",
            "message": "CountryCode is required",
            "details": {
                "Key": "CountryCode",
                "Property": "Destination.Address.CountryCode",
            },
        }
    ],
]


RateRequest = {
    "DeliveryReference": "ORDER123",
    "Destination": {
        "Address": {
            "Suburb": "Christchurch",
            "CountryCode": "NZ",
            "PostCode": "8061",
            "StreetAddress": "DestinationStreetAddress",
        },
        "ContactPerson": "DestinationName",
        "DeliveryInstructions": "Desinationdeliveryinstructions",
        "Email": "destinationemail@email.com",
        "PhoneNumber": "123456789",
        "RecipientTaxId": "123456",
    },
    "IsSaturdayDelivery": False,
    "IsSignatureRequired": True,
    "Packages": [
        {
            "Height": 1.0,
            "Kg": 0.1,
            "Length": 1.0,
            "Name": "SATCHEL",
            "Type": "Box",
            "Width": 10.0,
        }
    ],
}


RateResponse = """{
  "Available": [
    {
      "QuoteId": "e7fdf36c-8f6a-4d3f-8d96-c8b5893a0e7f",
      "CarrierId": 604,
      "CarrierName": "Omni Parcel",
      "DeliveryType": "AIR TRACKED",
      "Cost": 5.82,
      "ServiceStandard": "",
      "Comments": "",
      "Route": "OFFSHORE->AKL- SI",
      "IsRuralDelivery": false,
      "IsSaturdayDelivery": false,
      "IsFreightForward": false,
      "CarrierServiceType": "InternationalCourier"
    }
  ],
  "Rejected": [
    {
      "CarrierName": "CarrierName",
      "DeliveryType": "DeliveryType",
      "Reason": "Reason"
    }
  ],
  "ValidationErrors": {
    "Property": "Destination.Address.CountryCode",
    "Message": "CountryCode is required",
    "Key": "CountryCode",
    "Value": ""
  }
}
"""
