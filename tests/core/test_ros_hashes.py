from __future__ import annotations

import time

import pytest

pytest.importorskip("rclpy")
pytest.importorskip("rclpy._rclpy_pybind11")

import rclpy
import rclpy._rclpy_pybind11 as _impl
from rclpy.node import Node

from ros2_pyterfaces import DISTRO, Distro
from ros2_pyterfaces.core import CoreSchema, get_type_name, hash_rihs01, to_ros_type

from .utils import (
    MESSAGE_SCHEMA_IDS,
    MESSAGE_SCHEMAS,
    SERVICE_SCHEMA_IDS,
    SERVICE_SCHEMAS,
)

KNOWN_SERVICE_HASH_BY_TYPENAME: dict[str, str] = {
    "sensor_msgs/srv/SetCameraInfo": "RIHS01_a10cca5d33dc637c8d49db50ab288701a3592bb9cd854f2f16a0659613b68984",
    "std_srvs/srv/Trigger": "RIHS01_eeff2cd6fa5ad9d27cdf4dec64818317839b62f212a91e6b5304b634b2062c5f",
    "std_srvs/srv/SetBool": "RIHS01_abe9e4bb6b41b40e6789712c00ec8871923e089af3f667a79992a428cff2da0a",
}


IGNORED_MESSAGE_SCHEMA_TYPENAMES = set()
for schema in MESSAGE_SCHEMAS:
    try:
        to_ros_type(schema)
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError):
        IGNORED_MESSAGE_SCHEMA_TYPENAMES.add(get_type_name(schema))

MESSAGE_SCHEMA_PARAMS = [
    pytest.param(
        schema,
        id=schema_id,
        marks=(
            [pytest.mark.skip(reason=f"in ignore list: {get_type_name(schema)}")]
            if get_type_name(schema) in IGNORED_MESSAGE_SCHEMA_TYPENAMES
            else []
        ),
    )
    for schema, schema_id in zip(MESSAGE_SCHEMAS, MESSAGE_SCHEMA_IDS)
]
KNOWN_SERVICE_SCHEMAS = [
    schema
    for schema in SERVICE_SCHEMAS
    if get_type_name(schema) in KNOWN_SERVICE_HASH_BY_TYPENAME
]
KNOWN_SERVICE_SCHEMA_IDS = [
    schema_id
    for schema, schema_id in zip(SERVICE_SCHEMAS, SERVICE_SCHEMA_IDS)
    if get_type_name(schema) in KNOWN_SERVICE_HASH_BY_TYPENAME
]


@pytest.fixture(scope="module")
def ros_node() -> Node:
    rclpy.init()
    node = Node("core_hash_test_node")
    try:
        yield node
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


def _topic_for_type_name(type_name: str) -> str:
    safe_name = type_name.replace("/", "_")
    return f"/get_msg_hash/{safe_name}"


def _get_message_name_hash(node: Node, schema: CoreSchema) -> tuple[str, bytes]:
    ros_type = to_ros_type(schema)
    type_name = get_type_name(schema)
    topic = _topic_for_type_name(type_name)

    sub = node.create_subscription(ros_type, topic, lambda _msg: None, 10)
    try:
        for _ in range(50):
            rclpy.spin_once(node, timeout_sec=0.01)
            info = _impl.rclpy_get_subscriptions_info_by_topic(node.handle, topic, False)
            if info:
                return info[0]["topic_type"], info[0]["topic_type_hash"]["value"]
            time.sleep(0.01)
    finally:
        node.destroy_subscription(sub)

    raise LookupError(f"Unable to read subscription endpoint info for {type_name}")


@pytest.mark.skipif(DISTRO == Distro.HUMBLE, reason="Humble does not have type hashes")
@pytest.mark.parametrize("schema", MESSAGE_SCHEMA_PARAMS)
def test_message_hash_matches_ros(schema: CoreSchema, ros_node: Node) -> None:
    name, hash_value = _get_message_name_hash(ros_node, schema)
    assert get_type_name(schema) == name
    assert hash_rihs01(schema) == f"RIHS01_{hash_value.hex()}"


@pytest.mark.parametrize("schema", KNOWN_SERVICE_SCHEMAS, ids=KNOWN_SERVICE_SCHEMA_IDS)
def test_service_hash_matches_known_ros(schema: CoreSchema) -> None:
    type_name = get_type_name(schema)
    assert hash_rihs01(schema) == KNOWN_SERVICE_HASH_BY_TYPENAME[type_name]
