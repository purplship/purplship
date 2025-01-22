import karrio

gateway = karrio.gateway["seko"].create(
    dict(
        access_key="access_key",
        config=dict(cost_center="mysite.com", currency="GBP"),
    )
)
