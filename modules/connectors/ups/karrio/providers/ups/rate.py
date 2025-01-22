import karrio.schemas.ups.rating_request as ups
import karrio.schemas.ups.rating_response as rating
import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = provider_error.parse_error_response(response, settings)
    raw_rates = response.get("RateResponse", {}).get("RatedShipment") or []
    rates = [_extract_details(rate, settings, _response.ctx) for rate in raw_rates]

    return rates, messages


def _extract_details(
    detail: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> typing.List[models.RateDetails]:
    rate = lib.to_object(rating.RatedShipmentType, detail)
    effective_rate: typing.Union[
        rating.NegotiatedRateChargesType, rating.RatedShipmentType
    ] = lib.identity(
        rate.NegotiatedRateCharges if rate.NegotiatedRateCharges is not None else rate
    )
    total_charge: rating.BaseServiceChargeType = lib.identity(
        getattr(effective_rate, "TotalChargesWithTaxes", None)
        or getattr(effective_rate, "TotalCharges", None)
        or getattr(effective_rate, "TotalCharge", None)
        or rate.TransportationCharges
    )
    taxes = getattr(effective_rate, "TaxCharges", [])
    itemized_charges = [*effective_rate.ItemizedCharges, *taxes]

    charges = [
        ("BASE CHARGE", effective_rate.BaseServiceCharge.MonetaryValue),
        *lib.identity(
            []
            if any(itemized_charges)
            else [("Taxes", sum(lib.to_money(c.MonetaryValue) for c in taxes))]
        ),
        *lib.identity(
            [(rate.Service.Code, rate.ServiceOptionsCharges.MonetaryValue)]
            if lib.to_int(rate.ServiceOptionsCharges.MonetaryValue) > 0
            else []
        ),
        *lib.identity(
            (
                lib.identity(
                    provider_units.SurchargeType.map(
                        str(
                            getattr(c, "Code", None)
                            or getattr(c, "Type", None)
                            or "000"
                        )
                    )
                    .name_or_key.replace("_", " ")
                    .upper()
                ),
                c.MonetaryValue,
            )
            for c in itemized_charges
        ),
    ]

    transit_days = lib.failsafe(
        lambda: rate.TimeInTransit.ServiceSummary.EstimatedArrival.BusinessDaysInTransit,
    )
    currency = rate.TransportationCharges.CurrencyCode
    service = provider_units.ServiceZone.find(rate.Service.Code, ctx["origin"])

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=currency,
        service=service.name_or_key,
        total_charge=lib.to_money(total_charge.MonetaryValue),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(amount),
                currency=currency,
            )
            for name, amount in charges
            if name is not None or not amount
        ],
        transit_days=lib.to_int(transit_days),
        meta=dict(service_name=service.name_or_key),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address or payload.shipper)
    packages = lib.to_packages(payload.parcels, provider_units.PackagePresets)
    is_document = all([parcel.is_document for parcel in payload.parcels])
    service = lib.to_services(payload.services, provider_units.ServiceCode).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    currency = options.currency.state or settings.default_currency
    mps_packaging = lib.identity(
        provider_units.PackagingType.ups_unknown.value if len(packages) > 1 else None
    )
    weight_unit, dim_unit = lib.identity(
        provider_units.COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
        or packages.compatible_units
    )
    indications = [
        *(["01"] if options.pickup_options.state else []),
        *(["02"] if options.delivery_options.state else []),
    ]
    origin = lib.identity(
        "EU" if shipper.country_code in units.EUCountry else shipper.country_code
    )

    request = ups.RatingRequestType(
        RateRequest=ups.RateRequestType(
            Request=ups.RequestType(
                RequestOption="Shoptimeintransit",
                SubVersion="2205",
                TransactionReference=ups.TransactionReferenceType(
                    CustomerContext=payload.reference or "fetch rates",
                ),
            ),
            PickupType=None,
            CustomerClassification=None,
            Shipment=ups.ShipmentType(
                OriginRecordTransactionTimestamp=None,
                Shipper=ups.ShipType(
                    Name=shipper.name,
                    AttentionName=shipper.contact,
                    ShipperNumber=settings.account_number,
                    Address=ups.ShipFromAddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                    ),
                ),
                ShipTo=ups.ShipToType(
                    Name=recipient.name,
                    AttentionName=recipient.contact,
                    Address=ups.AlternateDeliveryAddressAddressType(
                        AddressLine=recipient.address_line,
                        City=recipient.city,
                        StateProvinceCode=recipient.state_code,
                        PostalCode=recipient.postal_code,
                        CountryCode=recipient.country_code,
                        ResidentialAddressIndicator=(
                            "Y" if recipient.residential else None
                        ),
                        POBoxIndicator=None,
                    ),
                ),
                ShipFrom=ups.ShipType(
                    Name=return_address.name,
                    AttentionName=return_address.contact,
                    Address=ups.ShipFromAddressType(
                        AddressLine=return_address.address_line,
                        City=return_address.city,
                        StateProvinceCode=return_address.state_code,
                        PostalCode=return_address.postal_code,
                        CountryCode=return_address.country_code,
                    ),
                ),
                AlternateDeliveryAddress=None,
                ShipmentIndicatorType=[
                    ups.CustomerClassificationType(Code=code, Description="Indicator")
                    for code in indications
                ],
                PaymentDetails=ups.PaymentDetailsType(
                    ShipmentCharge=ups.ShipmentChargeType(
                        Type="01",
                        BillShipper=ups.BillShipperType(
                            AccountNumber=settings.account_number,
                        ),
                        BillReceiver=None,
                        BillThirdParty=None,
                        ConsigneeBilledIndicator=None,
                    ),
                    SplitDutyVATIndicator=None,
                ),
                FRSPaymentInformation=None,
                FreightShipmentInformation=None,
                GoodsNotInFreeCirculationIndicator=None,
                Service=ups.CustomerClassificationType(
                    Code=(
                        service.value
                        if service
                        else provider_units.ServiceCode.ups_standard.value
                    ),
                    Description="Weight",
                ),
                NumOfPieces=None,  # Only required for Freight
                ShipmentTotalWeight=ups.WeightType(
                    UnitOfMeasurement=ups.CustomerClassificationType(
                        Code=provider_units.WeightUnit[packages.weight_unit].value,
                        Description="Dimension",
                    ),
                    Weight=str(packages.weight.value),
                ),  # Only required for "timeintransit" requests
                DocumentsOnlyIndicator=("Y" if is_document else None),
                Package=[
                    ups.PackageType(
                        PackagingType=ups.CustomerClassificationType(
                            Code=(
                                mps_packaging
                                or provider_units.PackagingType.map(
                                    package.packaging_type
                                ).value
                                or provider_units.PackagingType.ups_customer_supplied_package.value
                            ),
                            Description="Packaging Type",
                        ),
                        Dimensions=lib.identity(
                            ups.DimensionsType(
                                UnitOfMeasurement=ups.CustomerClassificationType(
                                    Code=dim_unit.value,
                                    Description="Dimension",
                                ),
                                Length=str(package.length[dim_unit.name]),
                                Width=str(package.width[dim_unit.name]),
                                Height=str(package.height[dim_unit.name]),
                            )
                            if any([package.length, package.width, package.height])
                            else None
                        ),
                        DimWeight=None,
                        PackageWeight=ups.WeightType(
                            UnitOfMeasurement=ups.CustomerClassificationType(
                                Code=provider_units.WeightUnit.map(
                                    weight_unit.name
                                ).value,
                                Description="Weight",
                            ),
                            Weight=str(package.weight[weight_unit.name]),
                        ),
                        Commodity=None,
                        PackageServiceOptions=lib.identity(
                            ups.PackageServiceOptionsType(
                                DeliveryConfirmation=lib.identity(
                                    ups.DeliveryConfirmationType(
                                        DCISType=options.ups_delivery_confirmation.state,
                                    )
                                    if options.ups_delivery_confirmation.state
                                    else None
                                ),
                            )
                            if options.ups_delivery_confirmation.state
                            else None
                        ),
                        UPSPremier=None,
                        OversizeIndicator=None,
                        MinimumBillableWeightIndicator=None,
                    )
                    for package in packages
                ],
                ShipmentServiceOptions=lib.identity(
                    ups.ShipmentServiceOptionsType(
                        SaturdayDeliveryIndicator=lib.identity(
                            "Y"
                            if options.ups_saturday_delivery_indicator.state
                            else None
                        ),
                        SaturdayPickupIndicator=lib.identity(
                            "Y" if options.ups_saturday_pickup_indicator.state else None
                        ),
                        SundayDeliveryIndicator=lib.identity(
                            "Y" if options.ups_sunday_delivery_indicator.state else None
                        ),
                        AvailableServicesOption=lib.identity(
                            options.ups_available_services_option.state
                        ),
                        AccessPointCOD=lib.identity(
                            ups.InvoiceLineTotalType(
                                CurrencyCode=options.currency.state,
                                MonetaryValue=lib.to_money(
                                    options.ups_access_point_cod.state
                                ),
                            )
                            if options.ups_access_point_cod.state
                            else None
                        ),
                        DeliverToAddresseeOnlyIndicator=lib.identity(
                            "Y"
                            if options.ups_deliver_to_addressee_only_indicator.state
                            else None
                        ),
                        DirectDeliveryOnlyIndicator=lib.identity(
                            "Y"
                            if options.ups_direct_delivery_only_indicator.state
                            else None
                        ),
                        COD=lib.identity(
                            ups.CodType(
                                CODFundsCode="0",  # TODO: find reference
                                CODAmount=ups.InvoiceLineTotalType(
                                    CurrencyCode=options.currency.state,
                                    MonetaryValue=str(options.cash_on_delivery.state),
                                ),
                            )
                            if options.ups_cod.state
                            else None
                        ),
                        DeliveryConfirmation=None,
                        ReturnOfDocumentIndicator=lib.identity(
                            "Y"
                            if options.ups_return_of_document_indicator.state
                            else None
                        ),
                        UPScarbonneutralIndicator=lib.identity(
                            "Y" if options.ups_carbonneutral_indicator.state else None
                        ),
                        CertificateOfOriginIndicator=lib.identity(
                            "Y"
                            if options.ups_certificate_of_origin_indicator.state
                            else None
                        ),
                        PickupOptions=lib.identity(
                            ups.PickupOptionsType(
                                HoldForPickupIndicator="Y",
                                LiftGateForPickUpIndicator=(
                                    "Y"
                                    if options.ups_lift_gate_for_pickup.state
                                    else None
                                ),
                            )
                            if options.pickup_options.state
                            else None
                        ),
                        DeliveryOptions=lib.identity(
                            ups.DeliveryOptionsType(
                                DropOffAtUPSFacilityIndicator="Y",
                                LiftGateForDeliveryIndicator=(
                                    "Y"
                                    if options.ups_lift_gate_for_delivery.state
                                    else None
                                ),
                            )
                            if options.delivery_options.state
                            else None
                        ),
                        RestrictedArticles=lib.identity(
                            ups.RestrictedArticlesType(
                                AlcoholicBeveragesIndicator=lib.identity(
                                    "Y"
                                    if options.ups_alcoholic_beverages_indicator.state
                                    else None
                                ),
                                DiagnosticSpecimensIndicator=lib.identity(
                                    "Y"
                                    if options.ups_diagnostic_specimens_indicator.state
                                    else None
                                ),
                                PerishablesIndicator=lib.identity(
                                    "Y"
                                    if options.ups_perishables_indicator.state
                                    else None
                                ),
                                PlantsIndicator=lib.identity(
                                    "Y" if options.ups_plants_indicator.state else None
                                ),
                                SeedsIndicator=lib.identity(
                                    "Y" if options.ups_seeds_indicator.state else None
                                ),
                                SpecialExceptionsIndicator=lib.identity(
                                    "Y"
                                    if (
                                        options.ups_special_exceptions_indicator.state
                                        or options.dangerous_goods.state
                                    )
                                    else None
                                ),
                                TobaccoIndicator=lib.identity(
                                    "Y" if options.ups_tobacco_indicator.state else None
                                ),
                            )
                            if options.ups_restricted_articles.state
                            else None
                        ),
                        ShipperExportDeclarationIndicator=lib.identity(
                            "Y"
                            if options.ups_shipper_export_declaration_indicator.state
                            else None
                        ),
                        CommercialInvoiceRemovalIndicator=lib.identity(
                            "Y"
                            if options.ups_commercial_invoice_removal_indicator.state
                            else None
                        ),
                        ImportControl=None,
                        ReturnService=None,
                        SDLShipmentIndicator=lib.identity(
                            "Y" if options.ups_sdl_shipment_indicator.state else None
                        ),
                        EPRAIndicator=lib.identity(
                            "Y" if options.ups_epra_indicator.state else None
                        ),
                        InsideDelivery=options.ups_inside_delivery.state,
                        ItemDisposalIndicator=lib.identity(
                            "Y" if options.ups_item_disposal.state else None
                        ),
                    )
                    if any(options.items())
                    else None
                ),
                ShipmentRatingOptions=ups.ShipmentRatingOptionsType(
                    NegotiatedRatesIndicator=lib.identity(
                        "Y"
                        if options.ups_negotiated_rates_indicator.state is not False
                        else None
                    ),
                    FRSShipmentIndicator=lib.identity(
                        "Y" if options.ups_frs_shipment_indicator.state else None
                    ),
                    RateChartIndicator=lib.identity(
                        "Y" if options.ups_rate_chart_indicator.state else None
                    ),
                    UserLevelDiscountIndicator=lib.identity(
                        "Y" if options.ups_user_level_discount_indicator.state else None
                    ),
                    TPFCNegotiatedRatesIndicator=lib.identity(
                        "Y"
                        if options.ups_tpfc_negotiated_rates_indicator.state
                        else None
                    ),
                ),
                InvoiceLineTotal=ups.InvoiceLineTotalType(
                    CurrencyCode=currency,
                    MonetaryValue=str(options.declared_value.state or 1.0),
                ),
                RatingMethodRequestedIndicator="Y",
                TaxInformationIndicator="Y",
                PromotionalDiscountInformation=None,
                DeliveryTimeInformation=ups.DeliveryTimeInformationType(
                    PackageBillType=("02" if is_document else "03"),
                    Pickup=ups.PickupType(
                        Date=lib.fdatetime(
                            options.shipment_date.state or time.strftime("%Y-%m-%d"),
                            current_format="%Y-%m-%d",
                            output_format="%Y%m%d",
                        )
                    ),
                ),
            ),
        )
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        ctx=dict(origin=origin),
    )
