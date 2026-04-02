import inspect
from collections.abc import Mapping
from typing import Any

from ros2_pyterfaces import DISTRO, Distro
from ros2_pyterfaces import core
from ros2_pyterfaces.cyclone import all_msgs
from ros2_pyterfaces.cyclone.idl import IdlStruct

NOT_IN_ROS = [
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
]
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


def _is_message_type(value: Any) -> bool:
    return inspect.isclass(value) and issubclass(value, IdlStruct) and value is not IdlStruct


def _collect_unique_message_types(namespace: Mapping[str, Any]) -> list[type[IdlStruct]]:
    by_typename: dict[str, type[IdlStruct]] = {}
    for value in namespace.values():
        if not _is_message_type(value):
            continue
        msg_type = value
        type_name = msg_type.get_type_name()
        if "/msg/" not in type_name:
            continue
        if type_name in EXCLUDED_MESSAGE_TYPES:
            continue
        by_typename.setdefault(type_name, msg_type)
    return [by_typename[type_name] for type_name in sorted(by_typename)]


def random_message_for_type(msg_type: type[IdlStruct], seed: int | None = None) -> IdlStruct:
    core_schema = msg_type.to_core_schema()
    core_msg = core.random_message(core_schema, seed=seed)
    return msg_type._from_core_message_dict(core_msg)


MESSAGE_TYPES: list[type[IdlStruct]] = _collect_unique_message_types(vars(all_msgs))
MESSAGE_TYPE_IDS: list[str] = [msg_type.get_type_name() for msg_type in MESSAGE_TYPES]
MESSAGE_VALUES: list[IdlStruct] = [random_message_for_type(msg_type) for msg_type in MESSAGE_TYPES]
MESSAGE_VALUE_IDS: list[str] = [type(msg).get_type_name() for msg in MESSAGE_VALUES]
