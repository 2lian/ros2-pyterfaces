import asyncio
from typing import Type

import asyncio_for_robotics.ros2 as afor
import pytest
import rclpy
from rclpy.subscription import Subscription

from .utils import TYPES, TYPES_IDS, VALUES, VALUES_IDS, assert_strictly_eq

from ros2_pyterfaces.cyclone import idl


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


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
async def test_send_raw(my_type: Type[idl.IdlStruct], init):
    res = await afor.soft_wait_for(send_raw(my_type, my_type.get_ros_type()), 3)
    assert not isinstance(res, TimeoutError)
    # assert res == my_type()
    assert idl.message_to_plain_data(res) == idl.message_to_plain_data(my_type())


@pytest.mark.parametrize("my_type", TYPES, ids=TYPES_IDS)
async def test_recv_raw(my_type: Type[idl.IdlStruct], init):
    res = await afor.soft_wait_for(recv_raw(my_type, my_type.get_ros_type()), 3)
    assert not isinstance(res, TimeoutError)
    # assert res == my_type()
    assert idl.message_to_plain_data(res) == idl.message_to_plain_data(my_type())


@pytest.mark.parametrize("my_msg", VALUES, ids=VALUES_IDS)
async def test_send_raw_values(my_msg: idl.IdlStruct, init):
    res = await afor.soft_wait_for(send_raw(my_msg, my_msg.get_ros_type()), 3)
    assert not isinstance(res, TimeoutError)
    # assert res == my_type()
    assert idl.message_to_plain_data(res) == idl.message_to_plain_data(my_msg)
