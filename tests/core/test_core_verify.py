from __future__ import annotations

import pytest

from ros2_pyterfaces.core import CoreSchema, Sequence, random_message, verify_message

from .utils import MESSAGE_SCHEMA_IDS, MESSAGE_SCHEMAS


@pytest.mark.parametrize("schema", MESSAGE_SCHEMAS, ids=MESSAGE_SCHEMA_IDS)
def test_verify_message_accepts_random_messages(schema: CoreSchema) -> None:
    core_msg = random_message(schema)

    assert verify_message(schema, core_msg) == []


def test_verify_message_reports_byte_scalar_type_issue() -> None:
    schema: CoreSchema = {
        "__typename": "pkg/msg/ByteScalar",
        "data": "byte",
    }
    core_msg = {
        "__typename": "pkg/msg/ByteScalar",
        "data": 7,
    }

    issues = verify_message(schema, core_msg)

    assert any("data expected (bytes | bytearray | memoryview) len == 1" in issue for issue in issues)


def test_verify_message_reports_byte_collection_type_issue() -> None:
    schema: CoreSchema = {
        "__typename": "pkg/msg/ByteSequence",
        "payload": Sequence("byte"),
    }
    core_msg = {
        "__typename": "pkg/msg/ByteSequence",
        "payload": [1, 2, 3],
    }

    issues = verify_message(schema, core_msg)

    assert any("payload expected (bytes | bytearray | memoryview)" in issue for issue in issues)


def test_verify_message_reports_missing_and_unexpected_keys() -> None:
    schema: CoreSchema = {
        "__typename": "pkg/msg/Shape",
        "x": "int32",
    }
    core_msg = {
        "__typename": "pkg/msg/Shape",
        "extra": 1,
    }

    issues = verify_message(schema, core_msg)

    assert "x missing" in issues
    assert "extra unexpected" in issues
