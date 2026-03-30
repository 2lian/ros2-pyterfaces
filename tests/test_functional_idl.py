import json
from typing import ClassVar

from ros2_pyterfaces import idl


class RosPlainNested:
    count: int

    def __init__(self):
        self.count = 0

    @classmethod
    def get_fields_and_field_types(cls):
        return {"count": "int64"}


class RosPlainMessage:
    child: RosPlainNested
    label: str

    def __init__(self):
        self.child = RosPlainNested()
        self.label = ""

    @classmethod
    def get_fields_and_field_types(cls):
        return {"child": "pkg/msg/PlainNested", "label": "string"}


class PlainNested:
    __idl_typename__ = "pkg/msg/PlainNested"

    IGNORED: ClassVar[int] = 7
    count: int

    def __init__(self, count: int = 0):
        self.count = count


class PlainMessage:
    __idl_typename__ = "pkg/msg/PlainMessage"

    VERSION: ClassVar[int] = 1
    child: PlainNested
    label: str

    def __init__(self, child: PlainNested | None = None, label: str = ""):
        self.child = PlainNested() if child is None else child
        self.label = label


IDL_TO_ROS = {
    PlainNested: RosPlainNested,
    PlainMessage: RosPlainMessage,
}


def test_plain_schema_json_type_description_ignores_classvars():
    description = json.loads(idl.json_type_description(PlainMessage))

    assert description["type_description"]["type_name"] == "pkg/msg/PlainMessage"
    assert [field["name"] for field in description["type_description"]["fields"]] == [
        "child",
        "label",
    ]
    assert [field["name"] for field in description["referenced_type_descriptions"][0]["fields"]] == [
        "count"
    ]


def test_plain_schema_to_ros_from_ros_with_explicit_mapping():
    msg = PlainMessage(child=PlainNested(count=3), label="ok")

    ros_msg = idl.to_ros(msg, idl_to_ros_types=IDL_TO_ROS)
    assert isinstance(ros_msg, RosPlainMessage)
    assert ros_msg.child.count == 3
    assert ros_msg.label == "ok"

    roundtrip = idl.from_ros(PlainMessage, ros_msg, idl_to_ros_types=IDL_TO_ROS)
    assert isinstance(roundtrip, PlainMessage)
    assert idl.message_to_plain_data(roundtrip) == idl.message_to_plain_data(msg)


def test_plain_schema_ros_helpers_use_explicit_mapping():
    assert idl.get_type_name(PlainMessage) == "pkg/msg/PlainMessage"
    assert idl.get_ros_type(PlainMessage, idl_to_ros_types=IDL_TO_ROS) is RosPlainMessage
    assert idl.has_ros_type(PlainMessage, idl_to_ros_types=IDL_TO_ROS) is True
    assert (
        idl.message_to_plain_data(RosPlainMessage(), PlainMessage)
        == idl.message_to_plain_data(PlainMessage())
    )
