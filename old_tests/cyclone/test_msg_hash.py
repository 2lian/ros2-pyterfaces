import inspect
import json
import subprocess
import time
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Tuple, Type

import pytest

pytest.importorskip("asyncio_for_robotics.ros2")
pytest.importorskip("rclpy")
pytest.importorskip("rclpy._rclpy_pybind11")

import asyncio_for_robotics.ros2 as afor
import rclpy
import rclpy._rclpy_pybind11 as _impl

from ros2_pyterfaces import DISTRO, Distro
from ros2_pyterfaces.cyclone import idl
from ros2_pyterfaces.cyclone import all_msgs
from ros2_pyterfaces.cyclone.all_msgs import (
    DiagnosticStatus,
    JointState,
    KeyValue,
    String,
    Trajectory,
    TrajectoryPoint,
)
from ros2_pyterfaces.cyclone.std_msgs.msg import Char, Empty, Float32

NOT_IMPL_TYPES = [Trajectory, TrajectoryPoint]
TYPES: List[Type[idl.IdlStruct]] = sorted(
    {
        obj
        for obj in vars(all_msgs).values()
        if inspect.isclass(obj)
        and issubclass(obj, idl.IdlStruct)
        and obj is not idl.IdlStruct
        and obj.has_ros_type()
    },
    key=lambda cls: cls.__name__,
)

# TYPES = [
#     Empty,
#     Float32,
#     TrajectoryPoint,
#     Trajectory,
#     Char,
#     DiagnosticStatus,
# ]


def get_name_hash(my_type: Type[idl.IdlStruct]) -> Tuple[str, str]:
    sub = afor.Sub(my_type.get_ros_type(), f"/get_msg_hash/{my_type.get_type_name()}")
    try:
        with afor.auto_session().lock() as node:
            info = _impl.rclpy_get_subscriptions_info_by_topic(
                node.handle, sub.topic_info.topic, False
            )
        # pprint(info)
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
    except:
        pass


@pytest.mark.parametrize("my_type", TYPES)
@pytest.mark.skipif(DISTRO==Distro.HUMBLE, reason="Humble does not have type hashes")
async def test_hashes(my_type: Type[idl.IdlStruct], init):
    try:
        name, hash = get_name_hash(my_type)
    except AttributeError as e:
        if "has no attribute" in str(e) and my_type in NOT_IMPL_TYPES:
            pytest.xfail(
                f"Message {my_type.get_type_name()} doesn't exist in ROS 2",
            )
        raise e

    assert my_type.get_type_name() == name
    assert my_type._hash_rihs01_raw().digest() == hash
