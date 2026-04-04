import time

import pytest

pytest.importorskip("rclpy")
pytest.importorskip("rclpy._rclpy_pybind11")

import rclpy
import rclpy._rclpy_pybind11 as _impl
from rclpy.node import Node

from ros2_pyterfaces import DISTRO, Distro
from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import MESSAGE_TYPE_PARAMS


@pytest.fixture(scope="module")
def ros_node() -> Node:
    rclpy.init()
    node = Node("cydr_hash_test_node")
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


def _get_message_name_hash(node: Node, msg_type: type[IdlStruct]) -> tuple[str, bytes]:
    ros_type = msg_type.to_ros_type()
    type_name = msg_type.get_type_name()
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
@pytest.mark.parametrize("msg_type", MESSAGE_TYPE_PARAMS)
def test_message_hash_matches_ros(msg_type: type[IdlStruct], ros_node: Node) -> None:
    name, hash_value = _get_message_name_hash(ros_node, msg_type)
    assert msg_type.get_type_name() == name
    assert msg_type.hash_rihs01() == f"RIHS01_{hash_value.hex()}"
