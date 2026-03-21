import array
import asyncio
import inspect
from dataclasses import fields, is_dataclass
from typing import List, Mapping, Sequence, Tuple, Type

import asyncio_for_robotics.ros2 as afor
import numpy as np
import pytest
import rclpy
from rclpy.subscription import Subscription
from utils import assert_strictly_eq

from ros2_pyterfaces import all_msgs, idl
from ros2_pyterfaces.all_msgs import (
    Char,
    DiagnosticStatus,
    Empty,
    Float32,
    Float64,
    Quaternion, KeyValue,
    Header,
    Imu,
    JointState,
    KeyValue,
    String,
    Trajectory,
    TrajectoryPoint,
    Time,
)

TYPES: List[Type[idl.IdlStruct]] = sorted(
    {
        obj
        for obj in vars(all_msgs).values()
        if inspect.isclass(obj)
        and issubclass(obj, idl.IdlStruct)
        and obj is not idl.IdlStruct
    },
    key=lambda cls: cls.__name__,
)
NOT_IN_ROS = [
    # not in ROS yet
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
]
TYPES = [t for t in TYPES if t.get_type_name() not in NOT_IN_ROS]
# TYPES = [Empty, JointState]


class RawSub(afor.Sub):
    def _resolve_sub(self, topic_info: afor.TopicInfo) -> Subscription:
        with self.session.lock() as node:
            return node.create_subscription(
                **topic_info.as_kwarg(), callback=self.callback_for_sub, raw=True
            )


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


async def send_raw(t: Type[idl.IdlStruct] | idl.IdlStruct, ros_t):
    tinfo = afor.TopicInfo(t.get_type_name(), ros_t)
    sub = afor.Sub(**tinfo.as_kwarg())

    async def periodic_pub():
        with afor.auto_session().lock() as node:
            pub = node.create_publisher(**tinfo.as_kwarg())
            if isinstance(t, idl.IdlStruct):
                pub.publish(t.serialize())
            else:
                pub.publish(t().serialize())

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(periodic_pub())
            recv = await sub.wait_for_value()
            res = t.from_ros(recv)
            return res
    finally:
        sub.close()


async def recv_raw(t: Type[idl.IdlStruct], ros_t):
    tinfo = afor.TopicInfo(t.get_type_name(), ros_t)
    sub = RawSub(**tinfo.as_kwarg())

    async def periodic_pub():
        with afor.auto_session().lock() as node:
            pub = node.create_publisher(**tinfo.as_kwarg())
            pub.publish(ros_t())

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(periodic_pub())
            recv = await sub.wait_for_value()
            res = t.deserialize(recv)
            return res
    finally:
        sub.close()


@pytest.mark.parametrize("my_type", TYPES)
async def test_send_raw(my_type: Type[idl.IdlStruct], init):
    res = await afor.soft_wait_for(send_raw(my_type, my_type.get_ros_type()), 3)
    assert not isinstance(res, TimeoutError)
    # assert res == my_type()
    assert_strictly_eq(res, my_type())


@pytest.mark.parametrize("my_type", TYPES)
async def test_recv_raw(my_type: Type[idl.IdlStruct], init):
    res = await afor.soft_wait_for(recv_raw(my_type, my_type.get_ros_type()), 3)
    assert not isinstance(res, TimeoutError)
    # assert res == my_type()
    assert_strictly_eq(res, my_type())


VALUES = [
    String(data="hello"),
    Char(3),
    Float32(np.float32(np.pi)),
    Float64(np.pi),
    JointState(
        header=Header(stamp=Time(1, 76)),
        position=list(range(100)),
        velocity=list(range(100)),
    ),
    Empty(),
    Imu(orientation=Quaternion(1, 0, 0, 0), orientation_covariance=np.full((9,), 0.1)),
    DiagnosticStatus(
        level=DiagnosticStatus.WARN,
        name="hey",
        message="hello",
        values=[KeyValue(key="heyyo", value="yey")],
    ),
]


@pytest.mark.parametrize("my_msg", VALUES)
async def test_send_raw_values(my_msg: idl.IdlStruct, init):
    res = await afor.soft_wait_for(send_raw(my_msg, my_msg.get_ros_type()), 3)
    assert not isinstance(res, TimeoutError)
    # assert res == my_type()
    assert_strictly_eq(res, my_msg)
