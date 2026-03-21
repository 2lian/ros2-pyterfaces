import array
from dataclasses import fields, is_dataclass
from typing import List, Mapping, Sequence, Tuple, Type

import numpy as np

from ros2_pyterfaces.idl import IdlStruct


def assert_strictly_eq(a: IdlStruct, b: IdlStruct):
    try:
        assert a == b
    except:
        assert_msg_equal_as_lists(a, b)


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

    # generic sequence -> list
    if isinstance(obj, Sequence) and not isinstance(
        obj, (str, bytes, bytearray, memoryview)
    ):
        return [_normalize(x) for x in obj]

    return obj
