import pytest

from .utils import SERVICE_TYPE_IDS, SERVICE_TYPES

KNOWN_SERVICE_HASH_BY_TYPENAME: dict[str, str] = {
    "sensor_msgs/srv/SetCameraInfo": "RIHS01_a10cca5d33dc637c8d49db50ab288701a3592bb9cd854f2f16a0659613b68984",
    "std_srvs/srv/Trigger": "RIHS01_eeff2cd6fa5ad9d27cdf4dec64818317839b62f212a91e6b5304b634b2062c5f",
    "std_srvs/srv/SetBool": "RIHS01_abe9e4bb6b41b40e6789712c00ec8871923e089af3f667a79992a428cff2da0a",
}

KNOWN_SERVICE_TYPES = [
    service_type
    for service_type in SERVICE_TYPES
    if service_type.get_type_name() in KNOWN_SERVICE_HASH_BY_TYPENAME
]
KNOWN_SERVICE_TYPE_IDS = [
    service_id
    for service_type, service_id in zip(SERVICE_TYPES, SERVICE_TYPE_IDS)
    if service_type.get_type_name() in KNOWN_SERVICE_HASH_BY_TYPENAME
]


@pytest.mark.parametrize(
    "service_type", KNOWN_SERVICE_TYPES, ids=KNOWN_SERVICE_TYPE_IDS
)
def test_service_hash_matches_known_ros(service_type: type) -> None:
    type_name = service_type.get_type_name()
    assert service_type.hash_rihs01() == KNOWN_SERVICE_HASH_BY_TYPENAME[type_name]
