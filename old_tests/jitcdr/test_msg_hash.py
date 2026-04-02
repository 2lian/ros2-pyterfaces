import inspect
from typing import List, Tuple, Type

import pytest

pytest.importorskip("cydr")
pytest.importorskip("asyncio_for_robotics.ros2")
pytest.importorskip("rclpy")
pytest.importorskip("rclpy._rclpy_pybind11")

import asyncio_for_robotics.ros2 as afor
import rclpy
import rclpy._rclpy_pybind11 as _impl

from ros2_pyterfaces import DISTRO, Distro
from ros2_pyterfaces.jitcdr import all_msgs
from ros2_pyterfaces.jitcdr.idl import JitStruct

NOT_IMPL_TYPES: list[type[JitStruct]] = []
NOT_IN_ROS = {
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
}
NOT_IN_HUMBLE = {
    "rcl_interfaces/msg/LoggerLevel",
    "rcl_interfaces/msg/SetLoggerLevelsResult",
    "service_msgs/msg/ServiceEventInfo",
    "type_description_interfaces/msg/Field",
    "type_description_interfaces/msg/FieldType",
    "type_description_interfaces/msg/IndividualTypeDescription",
    "type_description_interfaces/msg/KeyValue",
    "type_description_interfaces/msg/TypeDescription",
    "type_description_interfaces/msg/TypeSource",
}
EXCLUDED_MESSAGE_TYPES = set(NOT_IN_ROS)
if DISTRO == Distro.HUMBLE:
    EXCLUDED_MESSAGE_TYPES.update(NOT_IN_HUMBLE)

TYPES: List[Type[JitStruct]] = sorted(
    {
        obj
        for obj in vars(all_msgs).values()
        if inspect.isclass(obj)
        and issubclass(obj, JitStruct)
        and obj is not JitStruct
        and not getattr(obj, "__unsupported_reason__", None)
        and obj.get_type_name() not in EXCLUDED_MESSAGE_TYPES
        and obj.has_ros_type()
    },
    key=lambda cls: cls.__name__,
)


def get_name_hash(my_type: Type[JitStruct]) -> Tuple[str, str]:
    sub = afor.Sub(my_type.get_ros_type(), f"/get_msg_hash/{my_type.get_type_name()}")
    try:
        with afor.auto_session().lock() as node:
            info = _impl.rclpy_get_subscriptions_info_by_topic(
                node.handle, sub.topic_info.topic, False
            )
        return info[0]["topic_type"], info[0]["topic_type_hash"]["value"]
    finally:
        sub.close()


@pytest.fixture(scope="module")
def init():
    rclpy.init()
    ses = afor.auto_session()
    yield
    ses.close()
    try:
        rclpy.shutdown()
    except Exception:
        pass


@pytest.mark.parametrize("my_type", TYPES)
@pytest.mark.skipif(DISTRO == Distro.HUMBLE, reason="Humble does not have type hashes")
def test_hashes(my_type: Type[JitStruct], init):
    try:
        name, hash_value = get_name_hash(my_type)
    except AttributeError as exc:
        if "has no attribute" in str(exc) and my_type in NOT_IMPL_TYPES:
            pytest.xfail(
                f"Message {my_type.get_type_name()} doesn't exist in ROS 2",
            )
        raise exc

    assert my_type.get_type_name() == name
    assert my_type._hash_rihs01_raw().digest() == hash_value
