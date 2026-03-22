import inspect
from typing import List, Type

import pytest
from rclpy.serialization import deserialize_message, serialize_message
from utils import assert_msg_equal_as_lists, assert_strictly_eq

from ros2_pyterfaces import all_srvs, idl
from ros2_pyterfaces.all_srvs import (
    AddDiagnostics,
    AddDiagnostics_Request,
    AddDiagnostics_Response,
    GetInteractiveMarkers_Response,
    GetPlan_Request,
    LoadMap,
    LoadMap_Response,
    SelfTest_Response,
    SetBool,
    SetBool_Request,
    SetBool_Response,
    SetCameraInfo_Response,
)
from ros2_pyterfaces.diagnostic_msgs.msg import DiagnosticStatus
from ros2_pyterfaces.geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion
from ros2_pyterfaces.nav_msgs.msg import MapMetaData, OccupancyGrid
from ros2_pyterfaces.sensor_msgs.msg import CameraInfo
from ros2_pyterfaces.std_msgs.msg import Header
from ros2_pyterfaces.visualization_msgs.msg import InteractiveMarker

SERVICE_TYPES = [
    obj
    for obj in vars(all_srvs).values()
    if inspect.isclass(obj)
    and issubclass(obj, idl.IdlService)
    and obj is not idl.IdlService
]
REQUEST_RESPONSE_TYPES: List[Type[idl.IdlStruct]] = [
    obj
    for obj in vars(all_srvs).values()
    if inspect.isclass(obj)
    and issubclass(obj, idl.IdlStruct)
    and obj is not idl.IdlStruct
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
    GetInteractiveMarkers_Response(
        sequence_number=3,
        markers=[InteractiveMarker(name="control")],
    ),
]


@pytest.mark.parametrize("srv_type", SERVICE_TYPES)
def test_service_wrapper_matches_ros(srv_type: Type[idl.IdlService]):
    ros_srv_type = srv_type.get_ros_type()

    assert srv_type.to_ros_type() is ros_srv_type
    assert srv_type.Request.get_ros_type() is ros_srv_type.Request
    assert srv_type.Response.get_ros_type() is ros_srv_type.Response


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
    assert SetBool.Request is SetBool_Request
    assert SetBool.Response is SetBool_Response
    assert LoadMap.Response is LoadMap_Response
