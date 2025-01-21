from karrio.core.metadata import Metadata

from karrio.mappers.freightcom.mapper import Mapper
from karrio.mappers.freightcom.proxy import Proxy
from karrio.mappers.freightcom.settings import Settings
import karrio.providers.freightcom.units as units


METADATA = Metadata(
    id="freightcom",
    label="Freightcom",
    is_hub=True,
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService
)
