import karrio.schemas.freightcom.shipping_request as freightcom
import karrio.schemas.freightcom.shipping_response as shipping
import typing
import datetime
import uuid
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.freightcom.error as error
import karrio.providers.freightcom.utils as provider_utils
import karrio.providers.freightcom.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    """Parse Freightcom shipping response into Karrio format"""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # shipment = lib.to_multi_piece_shipment(
    #     [
    #         (index, _extract_details(data, data.get("shipmentId"), settings))
    #         for index, data in enumerate(response.get("labels", []))
    #     ]
    # )
    #

    shipment = _extract_details(response.get("shipment", {}), settings, ctx=_response.ctx) if "shipment" in response else None
    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShipmentType, data)
    label_type = "ZPL" if ctx["label_type"] == "ZPL" else "PDF"
    label_url = [_.url for _ in shipment.labels if _.format == label_type.lower() and _.size == "a6" and not _.padded]
    label = provider_utils.download_label(label_url[0]) if label_url else None
    tracking_numbers = (
        [
            shipment.primary_tracking_number
        ] +
        [
            tn for tn in shipment.tracking_numbers
            if tn != shipment.primary_tracking_number
        ]
    )

    rate = shipment.rate
    service = provider_units.ShippingService.map(
        rate.service_id,
    )

    courier = provider_units.ShippingCourier.find(rate.service_id)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.primary_tracking_number,
        shipment_identifier=shipment.id,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=shipment.tracking_url,
            tracking_numbers=tracking_numbers,
            rate_provider=courier.name_or_key,
            service_name=service.name_or_key,
            freightcom_service_id=rate.service_id,
            freightcom_unique_id=shipment.unique_id,

        )
    )


def create_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:


    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    packaging_type = provider_units.PackagingType.map(
        packages.package_type or "small_box"
    ).value

    is_intl = shipper.country_code != recipient.country_code
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
        default_to=(
            models.Customs(
                commodities=(
                    packages.items
                    if any(packages.items)
                    else [
                        models.Commodity(
                            quantity=1,
                            sku=f"000{index}",
                            weight=pkg.weight.value,
                            weight_unit=pkg.weight_unit.value,
                            description=pkg.parcel.content,
                        )
                        for index, pkg in enumerate(packages, start=1)
                    ]
                )
            )
            if is_intl
            else None
        ),
    )

    # TODO: need to know how to make this to get the payment_method ID, it's unique on each account, and not sure where this code belongs

    # payment_methods_response = proxy.get_payments_methods(lib.Serializable(None))
    # payment_methods = payment_methods_response.deserialize()
    #
    # # Get requested payment type or default to net_terms
    # requested_type = (payload.payment.type
    #                  if payload and payload.payment and payload.payment.type
    #                  else provider_units.PaymentMethodType.map().value)
    #
    # # Filter payment methods by type
    # filtered_methods = [
    #     method for method in payment_methods
    #     if method.get('type') == provider_units.PaymentMethodType.map(
    #         options.freightcom_payment_method or "net_terms"
    #     )
    # ]

    # payment_method_id = filtered_methods[0].get('id') if filtered_methods else payment_methods[0].get('id')
    #
    # if not payment_method_id:
    #     raise Exception("No payment method found")
    payment_method_id = '3PQtJaY49gIWzEVJ5DZrP8VP0vH1ZgWU'


    request = freightcom.ShippingRequestType(
        unique_id=str(uuid.uuid4()),
        payment_method_id=payment_method_id,
        service_id=provider_units.ShippingService.map(payload.service).value_or_key,
        details=freightcom.ShippingRequestDetailsType(
            origin=freightcom.DestinationType(
                name=shipper.company_name or shipper.person_name,
                address=freightcom.AddressType(
                    address_line_1=shipper.address_line1,
                    address_line_2=shipper.address_line2,
                    city=shipper.city,
                    region=shipper.state_code,
                    country=shipper.country_code,
                    postal_code=shipper.postal_code,
                ),
                residential=shipper.residential,
                contact_name=shipper.person_name if shipper.company_name else "",
                phone_number=freightcom.NumberType(
                    number=shipper.phone_number
                ) if shipper.phone_number else None,
                email_addresses=[shipper.email] if shipper.email else [],
            ),
            destination=freightcom.DestinationType(
                name=recipient.company_name or recipient.person_name,
                address=freightcom.AddressType(
                    address_line_1=recipient.address_line1,
                    address_line_2=recipient.address_line2,
                    city=recipient.city,
                    region=recipient.state_code,
                    country=recipient.country_code,
                    postal_code=recipient.postal_code,
                ),
                residential=recipient.residential,
                contact_name=recipient.person_name,
                phone_number=freightcom.NumberType(
                    number=recipient.phone_number
                ) if recipient.phone_number else None,
                email_addresses=[recipient.email] if recipient.email else [],
                ready_at=freightcom.ReadyType(
                    hour=lib.to_next_business_datetime(
                        options.shipping_date.state or datetime.datetime.now(),
                        current_format="%Y-%m-%dT%H:%M"
                    ).hour,
                    minute=0
                ),
                ready_until=freightcom.ReadyType(
                    hour=17,
                    minute=0
                ),
                signature_requirement="required" if options.signature_confirmation.state else "not-required"
            ),
            expected_ship_date=freightcom.DateType(
                year=lib.to_next_business_datetime(
                    options.shipping_date.state or datetime.datetime.now(),
                    current_format="%Y-%m-%dT%H:%M"
                ).year,
                month=lib.to_next_business_datetime(
                    options.shipping_date.state or datetime.datetime.now(),
                    current_format="%Y-%m-%dT%H:%M"
                ).month,
                day=lib.to_next_business_datetime(
                    options.shipping_date.state or datetime.datetime.now(),
                    current_format="%Y-%m-%dT%H:%M"
                ).day,
            ),
            packaging_type=packaging_type,
            packaging_properties=freightcom.PackagingPropertiesType(
                pallet_type="ltl" if packaging_type == "pallet" else None,
                has_stackable_pallets=options.stackable.state if packaging_type == "pallet" else None,
                dangerous_goods=options.dangerous_goods.state,
                dangerous_goods_details=freightcom.DangerousGoodsDetailsType(
                    packaging_group=options.dangerous_goods_group.state,
                    goods_class=options.dangerous_goods_class.state,
                ) if options.dangerous_goods.state else None,
                pallets=[
                    freightcom.PalletType(
                        measurements=freightcom.PackageMeasurementsType(
                            weight=freightcom.WeightType(
                                unit="kg",
                                value=parcel.weight.KG
                            ),
                            cuboid=freightcom.CuboidType(
                                unit="cm",
                                l=parcel.length.CM,
                                w=parcel.width.CM,
                                h=parcel.height.CM
                            )
                        ),
                        description=parcel.description or "N/A",
                        freight_class=options.freight_class.state,
                    ) for parcel in packages
                ] if packaging_type == "pallet" else [],
                packages=[
                    freightcom.PackageType(
                        measurements=freightcom.PackageMeasurementsType(
                            weight=freightcom.WeightType(
                                unit="kg",
                                value=parcel.weight.KG
                            ),
                            cuboid=freightcom.CuboidType(
                                unit="cm",
                                l=parcel.length.CM,
                                w=parcel.width.CM,
                                h=parcel.height.CM
                            )
                        ),
                        description=parcel.description or "N/A",
                    ) for parcel in packages
                ] if packaging_type == "package" else [],
                    courierpaks=[
                    freightcom.CourierpakType(
                        measurements=freightcom.CourierpakMeasurementsType(
                            weight=freightcom.WeightType(
                                unit="kg",
                                value=parcel.weight.KG
                            ),
                        ),
                        description=parcel.description or "N/A",
                    ) for parcel in packages
                ] if packaging_type == "courier-pak" else [],
            ),
            reference_codes=[payload.reference] if payload.reference else []
        ),
        customs_invoice=(
            freightcom.CustomsInvoiceType(
                source="details",
                broker=freightcom.BrokerType(
                  use_carrier=True,
                ),
                details=freightcom.CustomsInvoiceDetailsType(
                    products=[
                        freightcom.ProductType(
                            product_name=item.description,
                            weight=freightcom.WeightType(
                                unit="kg" if item.weight_unit.upper() == "KG" else "lb",
                                value=lib.to_decimal(item.weight)
                            ),
                            hs_code=item.hs_code,
                            country_of_origin=item.origin_country,
                            num_units=item.quantity,
                            unit_price=freightcom.TotalCostType(
                                currency=item.value_currency,
                                value=str(item.value_amount)
                            ),
                            description=item.description
                        ) for item in customs.commodities
                    ],
                    tax_recipient=freightcom.TaxRecipientType(
                        type=provider_units.PaymentType.map(
                                customs.duty.paid_by
                            ).value
                        or "shipper",
                        name=customs.duty_billing_address.company_name or customs.duty.person_name,
                        address=freightcom.AddressType(
                            address_line_1=customs.duty_billing_address.address_line1,
                            address_line_2=customs.duty_billing_address.address_line2,
                            city=customs.duty_billing_address.city,
                            region=customs.duty_billing_address.state_code,
                            country=customs.duty_billing_address.country_code,
                            postal_code=customs.duty_billing_address.postal_code,
                        ),
                        phone_number=freightcom.NumberType(
                            number=customs.duty_billing_address.phone_number
                        ),
                        reason_for_export=provider_units.CustomsContentType.map(
                            customs.content_type
                        ).value,
                    )
                )
            )
            if customs and customs.commodities
            else None
        ),
        #TODO: validate if we need to do pickup in the ship request
        # pickup_details=freightcom.PickupDetailsType(
        #
        # )
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=payload.label_type or "PDF")
    )
