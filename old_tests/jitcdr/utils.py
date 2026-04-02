import array
import inspect
from dataclasses import fields, is_dataclass
from typing import List, Mapping, Sequence, Type

import numpy as np
import pytest

pytest.importorskip("cydr")

from ros2_pyterfaces import DISTRO, Distro
from ros2_pyterfaces.cyclone import all_msgs as cyclone_all_msgs
from ros2_pyterfaces.jitcdr import all_msgs
from ros2_pyterfaces.jitcdr.idl import JitStruct
from ros2_pyterfaces.utils.random import random_message

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

CYCLONE_TYPES_BY_NAME = {
    obj.get_type_name(): obj
    for obj in vars(cyclone_all_msgs).values()
    if inspect.isclass(obj)
    and hasattr(obj, "get_type_name")
    and obj.get_type_name()
}

TYPES: List[Type[JitStruct]] = sorted(
    [
        obj
        for obj in vars(all_msgs).values()
        if inspect.isclass(obj)
        and issubclass(obj, JitStruct)
        and obj is not JitStruct
        and not getattr(obj, "__unsupported_reason__", None)
        and obj.get_type_name() not in EXCLUDED_MESSAGE_TYPES
        and obj.has_ros_type()
    ],
    key=lambda msg_type: msg_type.get_type_name(),
)
TYPES_IDS = [msg_type.get_type_name() for msg_type in TYPES]
VALUES: List[JitStruct] = [
    msg_type.from_ros(random_message(CYCLONE_TYPES_BY_NAME[msg_type.get_type_name()]).to_ros())
    for msg_type in TYPES
]
VALUES_IDS = [msg.get_type_name() for msg in VALUES]


def random_jit_message(msg_type: Type[JitStruct], seed: int | None = None) -> JitStruct:
    cyclone_type = CYCLONE_TYPES_BY_NAME[msg_type.get_type_name()]
    return msg_type.from_ros(random_message(cyclone_type, seed).to_ros())


def assert_strictly_eq(left, right) -> None:
    assert _normalize(left) == _normalize(right)


IGNORED_FIELDS = {}


def _normalize(obj):
    if hasattr(type(obj), "__struct_fields__") and not isinstance(obj, type):
        return {
            name: _normalize(getattr(obj, name))
            for name in type(obj).__struct_fields__
            if name not in IGNORED_FIELDS
        }

    if is_dataclass(obj) and not isinstance(obj, type):
        return {
            f.name: _normalize(getattr(obj, f.name))
            for f in fields(obj)
            if f.name not in IGNORED_FIELDS
        }

    getter = getattr(type(obj), "get_fields_and_field_types", None)
    if callable(getter):
        return {
            name: _normalize(getattr(obj, name))
            for name in getter().keys()
            if name not in IGNORED_FIELDS
        }

    if isinstance(obj, Mapping):
        return {k: _normalize(v) for k, v in obj.items()}

    if isinstance(obj, np.ndarray):
        return _normalize(obj.tolist())

    if isinstance(obj, array.array):
        return [_normalize(x) for x in obj.tolist()]

    if isinstance(obj, (bytes, bytearray, memoryview)):
        return [_normalize(x) for x in obj]

    if isinstance(obj, Sequence) and not isinstance(
        obj, (str, bytes, bytearray, memoryview)
    ):
        return [_normalize(x) for x in obj]

    return obj
