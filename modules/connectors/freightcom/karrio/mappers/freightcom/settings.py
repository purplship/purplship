"""Karrio freightcom connection settings."""

import attr
from karrio.providers.freightcom.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Freightcom connection settings."""

    username: str
    password: str
    api_key: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "freightcom"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
