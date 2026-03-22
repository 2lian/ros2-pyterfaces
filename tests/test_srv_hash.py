import inspect
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Tuple, Type

import asyncio_for_robotics.ros2 as afor
import pytest
import rclpy
import rclpy._rclpy_pybind11 as _impl
from std_srvs.srv import SetBool as RosSetBool

from ros2_pyterfaces import all_msgs, all_srvs, idl
from ros2_pyterfaces.all_srvs import SetBool_Request, SetBool_Response, Trigger


@dataclass
class SetBool_Event(idl.IdlStruct, typename="std_srvs/srv/SetBool_Event"):
    info: all_msgs.ServiceEventInfo = field(default_factory=all_msgs.ServiceEventInfo)
    request: idl.types.sequence[SetBool_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[SetBool_Response, 1] = field(default_factory=list)


@dataclass
class SetBool(idl.IdlStruct, typename="std_srvs/srv/SetBool"):
    request_message: SetBool_Request = field(
        default_factory=lambda *_: SetBool_Request()
    )
    response_message: SetBool_Response = field(
        default_factory=lambda *_: SetBool_Response()
    )
    event_message: SetBool_Event = field(default_factory=lambda *_: SetBool_Event())


TYPES_TO_HASH: dict[type[idl.IdlStruct], str] = {
    SetBool: "RIHS01_abe9e4bb6b41b40e6789712c00ec8871923e089af3f667a79992a428cff2da0a"
}


def debug(my_type: Type[idl.IdlStruct]) -> Tuple[str, str]:
    print(SetBool.json_type_description())
    print(SetBool.hash_rihs01())
    print(SetBool().request_message.hash_rihs01())
    print(SetBool().response_message.hash_rihs01())
    print(SetBool().event_message.hash_rihs01())
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
async def test_hashes(my_type: Type[idl.IdlStruct], init):
    assert my_type.hash_rihs01() == TYPES_TO_HASH[my_type]
