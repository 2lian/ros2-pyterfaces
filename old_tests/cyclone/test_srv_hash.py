import time
from dataclasses import dataclass, field
from typing import Tuple, Type, get_type_hints

import asyncio_for_robotics.ros2 as afor
import pytest
import rclpy

from ros2_pyterfaces.cyclone import idl
from ros2_pyterfaces.cyclone import all_msgs, all_srvs
from ros2_pyterfaces.cyclone.all_srvs import (
    SetBool,
    SetBool_Event,
    SetBool_Request,
    SetBool_Response,
    Trigger,
)
from ros2_pyterfaces.cyclone.sensor_msgs.srv import SetCameraInfo

HelperSetBool = idl.make_idl_service(
    SetBool_Request,
    SetBool_Response,
    event_type=SetBool_Event,
)

TYPES_TO_HASH: dict[type[idl.IdlStruct], str] = {
    SetCameraInfo: "RIHS01_a10cca5d33dc637c8d49db50ab288701a3592bb9cd854f2f16a0659613b68984",
    Trigger: "RIHS01_eeff2cd6fa5ad9d27cdf4dec64818317839b62f212a91e6b5304b634b2062c5f",
    SetBool: "RIHS01_abe9e4bb6b41b40e6789712c00ec8871923e089af3f667a79992a428cff2da0a",
    HelperSetBool: "RIHS01_abe9e4bb6b41b40e6789712c00ec8871923e089af3f667a79992a428cff2da0a",
}


def debug(my_type: Type[idl.IdlStruct]) -> Tuple[str, str]:
    print(Trigger.json_type_description())
    print(Trigger.hash_rihs01())
    print(Trigger().request_message.hash_rihs01())
    print(Trigger().response_message.hash_rihs01())
    print(Trigger().event_message.hash_rihs01())
    time.sleep(2)
    cli = afor.Client(
        my_type.get_ros_type(), f"/get_client_hash/{my_type.get_type_name()}"
    )
    time.sleep(2)
    srv = afor.Server(
        my_type.get_ros_type(), f"/get_client_hash/{my_type.get_type_name()}"
    )
    time.sleep(100000)
    try:
        pytest.skip()
        return info[0]["topic_type"], info[0]["topic_type_hash"]["value"]
    finally:
        srv.close()
        cli.close()


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


@pytest.mark.parametrize("my_type", TYPES_TO_HASH.keys())
async def test_hashes(my_type: type[idl.IdlStruct], init):
    # debug(my_type)
    assert my_type.hash_rihs01() == TYPES_TO_HASH[my_type]
