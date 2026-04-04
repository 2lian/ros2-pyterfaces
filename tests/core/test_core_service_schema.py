import json
import sys
import types
from typing import Any

import pytest

from ros2_pyterfaces.core import (
    Array,
    CoreSchema,
    from_ros,
    get_type_name,
    hash_rihs01,
    json_style_type_description,
    make_srv_schema,
    to_ros,
    to_ros_type,
)


class FakeTime:
    sec: int
    nanosec: int

    def __init__(self) -> None:
        self.sec = 0
        self.nanosec = 0


class FakeServiceEventInfo:
    event_type: int
    stamp: FakeTime
    client_gid: list[int]
    sequence_number: int

    def __init__(self) -> None:
        self.event_type = 0
        self.stamp = FakeTime()
        self.client_gid = []
        self.sequence_number = 0


class FakeSetBoolRequest:
    data: bool

    def __init__(self) -> None:
        self.data = False


class FakeSetBoolResponse:
    success: bool
    message: str

    def __init__(self) -> None:
        self.success = False
        self.message = ""


class FakeSetBoolEvent:
    info: FakeServiceEventInfo
    request: list[FakeSetBoolRequest]
    response: list[FakeSetBoolResponse]

    def __init__(self) -> None:
        self.info = FakeServiceEventInfo()
        self.request = []
        self.response = []


class FakeSetBoolService:
    Request = FakeSetBoolRequest
    Response = FakeSetBoolResponse
    Event = FakeSetBoolEvent


@pytest.fixture()
def fake_ros_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    builtin_interfaces_module = types.ModuleType("builtin_interfaces")
    builtin_interfaces_msg_module = types.ModuleType("builtin_interfaces.msg")
    builtin_interfaces_msg_module.Time = FakeTime
    builtin_interfaces_module.msg = builtin_interfaces_msg_module

    service_msgs_module = types.ModuleType("service_msgs")
    service_msgs_msg_module = types.ModuleType("service_msgs.msg")
    service_msgs_msg_module.ServiceEventInfo = FakeServiceEventInfo
    service_msgs_module.msg = service_msgs_msg_module

    pkg_module = types.ModuleType("pkg")
    pkg_srv_module = types.ModuleType("pkg.srv")
    pkg_srv_module.SetBool = FakeSetBoolService
    pkg_module.srv = pkg_srv_module

    monkeypatch.setitem(sys.modules, "builtin_interfaces", builtin_interfaces_module)
    monkeypatch.setitem(sys.modules, "builtin_interfaces.msg", builtin_interfaces_msg_module)
    monkeypatch.setitem(sys.modules, "service_msgs", service_msgs_module)
    monkeypatch.setitem(sys.modules, "service_msgs.msg", service_msgs_msg_module)
    monkeypatch.setitem(sys.modules, "pkg", pkg_module)
    monkeypatch.setitem(sys.modules, "pkg.srv", pkg_srv_module)


SETBOOL_REQUEST_SCHEMA: CoreSchema = {
    "__typename": "pkg/srv/SetBool_Request",
    "data": "bool",
}

SETBOOL_RESPONSE_SCHEMA: CoreSchema = {
    "__typename": "pkg/srv/SetBool_Response",
    "success": "bool",
    "message": "string",
}


def _service_core_message() -> dict[str, Any]:
    return {
        "__typename": "pkg/srv/SetBool",
        "request_message": {
            "__typename": "pkg/srv/SetBool_Request",
            "data": True,
        },
        "response_message": {
            "__typename": "pkg/srv/SetBool_Response",
            "success": True,
            "message": "ok",
        },
        "event_message": {
            "__typename": "pkg/srv/SetBool_Event",
            "info": {
                "__typename": "service_msgs/msg/ServiceEventInfo",
                "event_type": 1,
                "stamp": {
                    "__typename": "builtin_interfaces/msg/Time",
                    "sec": 9,
                    "nanosec": 10,
                },
                "client_gid": [0] * 16,
                "sequence_number": 42,
            },
            "request": {
                "__typename": "pkg/srv/SetBool_Request",
                "data": True,
            },
            "response": {
                "__typename": "pkg/srv/SetBool_Response",
                "success": True,
                "message": "ok",
            },
        },
    }


def test_make_srv_schema_builds_setbool_shape() -> None:
    schema = make_srv_schema(SETBOOL_REQUEST_SCHEMA, SETBOOL_RESPONSE_SCHEMA)

    assert schema["__typename"] == "pkg/srv/SetBool"
    assert schema["request_message"] is SETBOOL_REQUEST_SCHEMA
    assert schema["response_message"] is SETBOOL_RESPONSE_SCHEMA
    assert isinstance(schema["event_message"], dict)
    event_schema = schema["event_message"]
    assert event_schema["__typename"] == "pkg/srv/SetBool_Event"
    assert event_schema["request"] is SETBOOL_REQUEST_SCHEMA
    assert event_schema["response"] is SETBOOL_RESPONSE_SCHEMA
    assert event_schema["info"]["__typename"] == "service_msgs/msg/ServiceEventInfo"
    assert event_schema["info"]["client_gid"] == Array("uint8", 16)


def test_service_schema_metadata_functions() -> None:
    schema = make_srv_schema(SETBOOL_REQUEST_SCHEMA, SETBOOL_RESPONSE_SCHEMA)
    description = json_style_type_description(schema)

    assert get_type_name(schema) == "pkg/srv/SetBool"
    assert description["type_description"]["type_name"] == "pkg/srv/SetBool"
    referenced = description["referenced_type_descriptions"]
    referenced_type_names = [entry["type_name"] for entry in referenced]
    assert "pkg/srv/SetBool_Request" in referenced_type_names
    assert "pkg/srv/SetBool_Response" in referenced_type_names
    assert "pkg/srv/SetBool_Event" in referenced_type_names
    assert "service_msgs/msg/ServiceEventInfo" in referenced_type_names
    assert "builtin_interfaces/msg/Time" in referenced_type_names
    assert hash_rihs01(schema).startswith("RIHS01_")
    assert len(hash_rihs01(schema)) == len("RIHS01_" + ("a" * 64))
    json.dumps(description)


def test_service_schema_to_ros_type_and_roundtrip(fake_ros_modules: None) -> None:
    schema = make_srv_schema(SETBOOL_REQUEST_SCHEMA, SETBOOL_RESPONSE_SCHEMA)

    assert to_ros_type(schema) is FakeSetBoolService
    assert to_ros_type(SETBOOL_REQUEST_SCHEMA) is FakeSetBoolRequest
    assert to_ros_type(SETBOOL_RESPONSE_SCHEMA) is FakeSetBoolResponse
    assert to_ros_type(schema["event_message"]) is FakeSetBoolEvent

    core_service_msg = _service_core_message()
    ros_payload = to_ros(core_service_msg)

    assert isinstance(ros_payload, dict)
    assert isinstance(ros_payload["request_message"], FakeSetBoolRequest)
    assert isinstance(ros_payload["response_message"], FakeSetBoolResponse)
    assert isinstance(ros_payload["event_message"], FakeSetBoolEvent)
    assert len(ros_payload["event_message"].request) == 1
    assert len(ros_payload["event_message"].response) == 1

    back_to_core = from_ros(schema, ros_payload)
    assert back_to_core == core_service_msg
