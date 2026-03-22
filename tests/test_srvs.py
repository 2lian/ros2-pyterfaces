import inspect
import json
from typing import List, Type, get_type_hints

import pytest
from rclpy.serialization import deserialize_message, serialize_message
from utils import assert_msg_equal_as_lists, assert_strictly_eq

from ros2_pyterfaces import all_srvs, idl
from ros2_pyterfaces.all_srvs import (
    AddDiagnostics,
    AddDiagnostics_Request,
    AddDiagnostics_Response,
    GetTypeDescription,
    GetTypeDescription_Event,
    GetTypeDescription_Request,
    GetTypeDescription_Response,
    GetInteractiveMarkers_Response,
    GetPlan_Request,
    LoadMap,
    LoadMap_Response,
    SelfTest_Response,
    SetBool,
    SetBool_Request,
    SetBool_Response,
    SetCameraInfo_Response,
    Trigger,
)
from ros2_pyterfaces.diagnostic_msgs.msg import DiagnosticStatus
from ros2_pyterfaces.geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion
from ros2_pyterfaces.nav_msgs.msg import MapMetaData, OccupancyGrid
from ros2_pyterfaces.sensor_msgs.msg import CameraInfo
from ros2_pyterfaces.std_msgs.msg import Header
from ros2_pyterfaces.type_description_interfaces.msg import (
    Field,
    FieldType,
    IndividualTypeDescription,
    KeyValue,
    TypeDescription,
    TypeSource,
)
from ros2_pyterfaces.visualization_msgs.msg import InteractiveMarker

SERVICE_TYPES = [
    obj
    for obj in vars(all_srvs).values()
    if inspect.isclass(obj) and idl.is_service_type(obj)
]
REQUEST_RESPONSE_TYPES: List[Type[idl.IdlStruct]] = [
    obj
    for obj in vars(all_srvs).values()
    if inspect.isclass(obj)
    and issubclass(obj, idl.IdlStruct)
    and obj is not idl.IdlStruct
    and not idl.is_service_type(obj)
]

VALUES = [
    SetBool_Request(data=True),
    SetBool_Response(success=True, message="done"),
    AddDiagnostics_Request(load_namespace="/robot/diagnostics"),
    AddDiagnostics_Response(success=True, message="loaded"),
    SelfTest_Response(
        id="motor-check",
        passed=1,
        status=[
            DiagnosticStatus(
                level=DiagnosticStatus.OK,
                name="motor",
                message="ok",
            )
        ],
    ),
    GetPlan_Request(
        start=PoseStamped(
            header=Header(frame_id="map"),
            pose=Pose(position=Point(1, 2, 0), orientation=Quaternion(1, 0, 0, 0)),
        ),
        goal=PoseStamped(
            header=Header(frame_id="map"),
            pose=Pose(position=Point(3, 4, 0), orientation=Quaternion(1, 0, 0, 0)),
        ),
        tolerance=1,
    ),
    LoadMap_Response(
        map=OccupancyGrid(info=MapMetaData(width=2, height=2), data=[0, 100, -1, 0]),
        result=LoadMap_Response.RESULT_SUCCESS,
    ),
    SetCameraInfo_Response(success=True, status_message="stored"),
    GetTypeDescription_Request(
        type_name="std_msgs/msg/String",
        type_hash="RIHS01_123",
        include_type_sources=False,
    ),
    GetTypeDescription_Response(
        successful=True,
        type_description=TypeDescription(
            type_description=IndividualTypeDescription(
                type_name="std_msgs/msg/String",
                fields=[
                    Field(
                        name="data",
                        type=FieldType(type_id=FieldType.FIELD_TYPE_STRING),
                        default_value="",
                    )
                ],
            )
        ),
        type_sources=[
            TypeSource(
                type_name="std_msgs/msg/String",
                encoding="msg",
                raw_file_contents="string data\n",
            )
        ],
        extra_information=[KeyValue(key="schema", value="test")],
    ),
    GetInteractiveMarkers_Response(
        sequence_number=3,
        markers=[InteractiveMarker(name="control")],
    ),
]


@pytest.mark.parametrize("srv_type", SERVICE_TYPES)
def test_service_wrapper_matches_ros(srv_type: Type[idl.IdlStruct]):
    ros_srv_type = srv_type.get_ros_type()
    type_hints = get_type_hints(srv_type)

    assert srv_type.to_ros_type() is ros_srv_type
    assert type_hints["request_message"].get_ros_type() is ros_srv_type.Request
    assert type_hints["response_message"].get_ros_type() is ros_srv_type.Response


@pytest.mark.parametrize("msg_type", REQUEST_RESPONSE_TYPES)
def test_service_messages_to_ros_defaults(msg_type: Type[idl.IdlStruct]):
    ros_msg_type = msg_type.get_ros_type()
    ros_msg = msg_type().to_ros()

    assert isinstance(ros_msg, ros_msg_type)
    assert_msg_equal_as_lists(ros_msg, ros_msg_type())


@pytest.mark.parametrize("msg_type", REQUEST_RESPONSE_TYPES)
def test_service_messages_from_ros_defaults(msg_type: Type[idl.IdlStruct]):
    ros_msg_type = msg_type.get_ros_type()
    idl_msg = msg_type.from_ros(ros_msg_type())

    assert_strictly_eq(idl_msg, msg_type())


@pytest.mark.parametrize("msg_type", REQUEST_RESPONSE_TYPES)
def test_service_deserialize(msg_type: Type[idl.IdlStruct]):
    ros_msg_type = msg_type.get_ros_type()
    idl_from_ros = msg_type.deserialize(serialize_message(ros_msg_type()))

    assert_strictly_eq(idl_from_ros, msg_type())


@pytest.mark.parametrize("msg_type", REQUEST_RESPONSE_TYPES)
def test_service_serialize(msg_type: Type[idl.IdlStruct]):
    ros_msg_type = msg_type.get_ros_type()
    ros_from_idl = deserialize_message(msg_type().serialize(), ros_msg_type)

    assert_msg_equal_as_lists(ros_from_idl, ros_msg_type())


@pytest.mark.parametrize("msg", VALUES)
def test_service_messages_to_from_ros_values(msg: idl.IdlStruct):
    ros_msg = msg.to_ros()

    assert isinstance(ros_msg, type(msg).get_ros_type())
    assert_strictly_eq(type(msg).from_ros(ros_msg), msg)


@pytest.mark.parametrize("msg", VALUES)
def test_service_deserialize_values(msg: idl.IdlStruct):
    idl_from_ros = type(msg).deserialize(serialize_message(msg.to_ros()))

    assert_strictly_eq(idl_from_ros, msg)


@pytest.mark.parametrize("msg", VALUES)
def test_service_serialize_values(msg: idl.IdlStruct):
    ros_msg_type = msg.get_ros_type()
    ros_from_idl = deserialize_message(msg.serialize(), ros_msg_type)

    assert_strictly_eq(type(msg).from_ros(ros_from_idl), msg)
    assert_strictly_eq(type(msg).deserialize(serialize_message(ros_from_idl)), msg)


def test_service_wrapper_request_response_links():
    setbool_hints = get_type_hints(SetBool)
    load_map_hints = get_type_hints(LoadMap)
    get_type_description_hints = get_type_hints(GetTypeDescription)

    assert SetBool.Request is SetBool_Request
    assert SetBool.Response is SetBool_Response
    assert LoadMap.Response is LoadMap_Response
    assert setbool_hints["request_message"] is SetBool_Request
    assert setbool_hints["response_message"] is SetBool_Response
    assert setbool_hints["event_message"].get_type_name() == "std_srvs/srv/SetBool_Event"
    assert load_map_hints["response_message"] is LoadMap_Response
    assert get_type_description_hints["request_message"] is GetTypeDescription_Request
    assert (
        get_type_description_hints["response_message"] is GetTypeDescription_Response
    )
    assert GetTypeDescription.Request is GetTypeDescription_Request
    assert GetTypeDescription.Response is GetTypeDescription_Response


def test_all_srvs_exposes_event_types():
    assert issubclass(GetTypeDescription_Event, idl.IdlStruct)


def test_get_type_description_request_defaults_to_include_type_sources():
    request = GetTypeDescription_Request()

    assert request.include_type_sources is True
    assert request.to_ros().include_type_sources is True


def test_trigger_request_type_description_uses_placeholder_member():
    type_description = json.loads(Trigger.json_type_description())
    referenced = {
        desc["type_name"]: desc for desc in type_description["referenced_type_descriptions"]
    }
    trigger_request = referenced["std_srvs/srv/Trigger_Request"]

    assert trigger_request["fields"] == [
        {
            "name": "structure_needs_at_least_one_member",
            "type": {
                "type_id": 3,
                "capacity": 0,
                "string_capacity": 0,
                "nested_type_name": "",
            },
            "default_value": "",
        }
    ]
