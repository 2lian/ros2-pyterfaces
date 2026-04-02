import importlib
import json

import pytest

from ros2_pyterfaces.core import (
    CoreSchema,
    Sequence,
    get_type_name,
    hash_rihs01,
    json_style_type_description,
    json_type_description,
    to_ros_type,
)


def _field(
    *,
    name: str,
    type_id: int,
    capacity: int = 0,
    string_capacity: int = 0,
    nested_type_name: str = "",
) -> dict[str, object]:
    return {
        "name": name,
        "type": {
            "type_id": type_id,
            "capacity": capacity,
            "string_capacity": string_capacity,
            "nested_type_name": nested_type_name,
        },
        "default_value": "",
    }


TIME_SCHEMA: CoreSchema = {
    "__typename": "builtin_interfaces/msg/Time",
    "sec": "int32",
    "nanosec": "uint32",
}

HEADER_SCHEMA: CoreSchema = {
    "__typename": "std_msgs/msg/Header",
    "stamp": TIME_SCHEMA,
    "frame_id": "string",
}

JOINT_STATE_SCHEMA: CoreSchema = {
    "__typename": "sensor_msgs/msg/JointState",
    "header": HEADER_SCHEMA,
    "name": Sequence("string"),
    "position": Sequence("float64"),
    "velocity": Sequence("float64"),
    "effort": Sequence("float64"),
}


CASES: list[tuple[CoreSchema, dict[str, object], str]] = [
    (
        TIME_SCHEMA,
        {
            "type_description": {
                "type_name": "builtin_interfaces/msg/Time",
                "fields": [
                    _field(name="sec", type_id=6),
                    _field(name="nanosec", type_id=7),
                ],
            },
            "referenced_type_descriptions": [],
        },
        "RIHS01_b106235e25a4c5ed35098aa0a61a3ee9c9b18d197f398b0e4206cea9acf9c197",
    ),
    (
        HEADER_SCHEMA,
        {
            "type_description": {
                "type_name": "std_msgs/msg/Header",
                "fields": [
                    _field(
                        name="stamp",
                        type_id=1,
                        nested_type_name="builtin_interfaces/msg/Time",
                    ),
                    _field(name="frame_id", type_id=17),
                ],
            },
            "referenced_type_descriptions": [
                {
                    "type_name": "builtin_interfaces/msg/Time",
                    "fields": [
                        _field(name="sec", type_id=6),
                        _field(name="nanosec", type_id=7),
                    ],
                }
            ],
        },
        "RIHS01_f49fb3ae2cf070f793645ff749683ac6b06203e41c891e17701b1cb597ce6a01",
    ),
    (
        JOINT_STATE_SCHEMA,
        {
            "type_description": {
                "type_name": "sensor_msgs/msg/JointState",
                "fields": [
                    _field(
                        name="header",
                        type_id=1,
                        nested_type_name="std_msgs/msg/Header",
                    ),
                    _field(name="name", type_id=161),
                    _field(name="position", type_id=155),
                    _field(name="velocity", type_id=155),
                    _field(name="effort", type_id=155),
                ],
            },
            "referenced_type_descriptions": [
                {
                    "type_name": "builtin_interfaces/msg/Time",
                    "fields": [
                        _field(name="sec", type_id=6),
                        _field(name="nanosec", type_id=7),
                    ],
                },
                {
                    "type_name": "std_msgs/msg/Header",
                    "fields": [
                        _field(
                            name="stamp",
                            type_id=1,
                            nested_type_name="builtin_interfaces/msg/Time",
                        ),
                        _field(name="frame_id", type_id=17),
                    ],
                },
            ],
        },
        "RIHS01_a13ee3a330e346c9d87b5aa18d24e11690752bd33a0350f11c5882bc9179260e",
    ),
]

CASE_IDS = [case[0]["__typename"] for case in CASES]


@pytest.mark.parametrize(("schema", "expected_description", "_"), CASES, ids=CASE_IDS)
def test_json_style_type_description(
    schema: CoreSchema,
    expected_description: dict[str, object],
    _: str,
) -> None:
    assert get_type_name(schema) == schema["__typename"]
    assert json_style_type_description(schema) == expected_description
    assert json.loads(json_type_description(schema)) == expected_description


@pytest.mark.parametrize(("schema", "_", "expected_hash"), CASES, ids=CASE_IDS)
def test_hash_rihs01(schema: CoreSchema, _: dict[str, object], expected_hash: str) -> None:
    assert hash_rihs01(schema) == expected_hash


@pytest.mark.parametrize(("schema", "_", "__"), CASES, ids=CASE_IDS)
def test_to_ros_type(schema: CoreSchema, _: dict[str, object], __: str) -> None:
    pytest.importorskip("builtin_interfaces.msg")
    pytest.importorskip("std_msgs.msg")
    pytest.importorskip("sensor_msgs.msg")

    type_name = get_type_name(schema)
    module_name, class_name = type_name.replace("/", ".").rsplit(".", 1)
    expected_type = getattr(importlib.import_module(module_name), class_name)
    assert to_ros_type(schema) is expected_type
