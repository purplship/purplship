import karrio

gateway = karrio.gateway["freightcom"].create(
    dict(
        username="username",
        password="password",
        api_key="api_key",
    )
)
