import array
import inspect
from dataclasses import fields, is_dataclass
from typing import List, Mapping, Sequence, Type

import numpy as np

from ros2_pyterfaces import all_msgs, idl
from ros2_pyterfaces.idl import IdlStruct
from ros2_pyterfaces.utils.random import random_message

NOT_IN_ROS = [
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
]
TYPES: List[Type[idl.IdlStruct]] = sorted(
    [
        obj
        for obj in vars(all_msgs).values()
        if inspect.isclass(obj)
        and issubclass(obj, idl.IdlStruct)
        and obj is not idl.IdlStruct
        and obj.get_type_name() not in NOT_IN_ROS
    ],
    key=lambda msg_type: msg_type.get_type_name(),
)
TYPES_IDS = [msg_type.get_type_name() for msg_type in TYPES]
VALUES: List[idl.IdlStruct] = [random_message(msg_type) for msg_type in TYPES]
VALUES_IDS = [msg.get_type_name() for msg in VALUES]


def assert_strictly_eq(a: IdlStruct, b: IdlStruct):
    assert idl.message_to_plain_data(a) == idl.message_to_plain_data(b)


IGNORED_FIELDS = {}


def assert_msg_equal_as_lists(left, right) -> None:
    left_norm = _normalize(left)
    right_norm = _normalize(right)
    assert left_norm == right_norm


def _normalize(obj):
    # Dataclass -> dict
    if is_dataclass(obj) and not isinstance(obj, type):
        return {
            f.name: _normalize(getattr(obj, f.name))
            for f in fields(obj)
            if f.name not in IGNORED_FIELDS
        }

    # ROS message object -> dict of fields
    getter = getattr(type(obj), "get_fields_and_field_types", None)
    if callable(getter):
        return {
            name: _normalize(getattr(obj, name))
            for name in getter().keys()
            if name not in IGNORED_FIELDS
        }

    # Mapping -> dict
    if isinstance(obj, Mapping):
        return {k: _normalize(v) for k, v in obj.items()}

    # numpy array -> list
    if isinstance(obj, np.ndarray):
        return _normalize(obj.tolist())

    # array.array -> list
    if isinstance(obj, array.array):
        return [_normalize(x) for x in obj.tolist()]

    # bytes-like -> list[int]
    if isinstance(obj, (bytes, bytearray, memoryview)):
        return [_normalize(x) for x in obj]

    # generic sequence -> list
    if isinstance(obj, Sequence) and not isinstance(
        obj, (str, bytes, bytearray, memoryview)
    ):
        return [_normalize(x) for x in obj]

    return obj
