import inspect
from collections.abc import Mapping
from typing import Any

import pytest

from ros2_pyterfaces import DISTRO, Distro, core
from ros2_pyterfaces.cydr import all_msgs, all_srvs
from ros2_pyterfaces.cydr.idl import IdlStruct

NOT_IN_ROS = [
    "nav_msgs/msg/Trajectory",
    "nav_msgs/msg/TrajectoryPoint",
    "test_msgs/msg/Builtins",
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

IGNORED_MESSAGE_TYPES = set(NOT_IN_ROS)
if DISTRO == Distro.HUMBLE:
    IGNORED_MESSAGE_TYPES.update(NOT_IN_HUMBLE)

NOT_IN_ROS_SERVICE_TYPES: set[str] = set()
NOT_IN_HUMBLE_SERVICE_TYPES = {
    "rcl_interfaces/srv/GetLoggerLevels",
    "rcl_interfaces/srv/SetLoggerLevels",
    "type_description_interfaces/srv/GetTypeDescription",
}
IGNORED_SERVICE_TYPES = set(NOT_IN_ROS_SERVICE_TYPES)
if DISTRO == Distro.HUMBLE:
    IGNORED_SERVICE_TYPES.update(NOT_IN_HUMBLE_SERVICE_TYPES)

NOT_IN_ROS_SERVICE_MESSAGE_TYPES: set[str] = set()
NOT_IN_HUMBLE_SERVICE_MESSAGE_TYPES = {
    "composition_interfaces/srv/ListNodes_Event",
    "composition_interfaces/srv/LoadNode_Event",
    "composition_interfaces/srv/UnloadNode_Event",
    "diagnostic_msgs/srv/AddDiagnostics_Event",
    "diagnostic_msgs/srv/SelfTest_Event",
    "lifecycle_msgs/srv/ChangeState_Event",
    "lifecycle_msgs/srv/GetAvailableStates_Event",
    "lifecycle_msgs/srv/GetAvailableTransitions_Event",
    "lifecycle_msgs/srv/GetState_Event",
    "nav_msgs/srv/GetMap_Event",
    "nav_msgs/srv/GetPlan_Event",
    "nav_msgs/srv/LoadMap_Event",
    "nav_msgs/srv/SetMap_Event",
    "rcl_interfaces/srv/DescribeParameters_Event",
    "rcl_interfaces/srv/GetLoggerLevels_Event",
    "rcl_interfaces/srv/GetLoggerLevels_Request",
    "rcl_interfaces/srv/GetLoggerLevels_Response",
    "rcl_interfaces/srv/GetParameterTypes_Event",
    "rcl_interfaces/srv/GetParameters_Event",
    "rcl_interfaces/srv/ListParameters_Event",
    "rcl_interfaces/srv/SetLoggerLevels_Event",
    "rcl_interfaces/srv/SetLoggerLevels_Request",
    "rcl_interfaces/srv/SetLoggerLevels_Response",
    "rcl_interfaces/srv/SetParametersAtomically_Event",
    "rcl_interfaces/srv/SetParameters_Event",
    "sensor_msgs/srv/SetCameraInfo_Event",
    "std_srvs/srv/Empty_Event",
    "std_srvs/srv/SetBool_Event",
    "std_srvs/srv/Trigger_Event",
    "type_description_interfaces/srv/GetTypeDescription_Event",
    "type_description_interfaces/srv/GetTypeDescription_Request",
    "type_description_interfaces/srv/GetTypeDescription_Response",
    "visualization_msgs/srv/GetInteractiveMarkers_Event",
}
IGNORED_SERVICE_MESSAGE_TYPES = set(NOT_IN_ROS_SERVICE_MESSAGE_TYPES)
if DISTRO == Distro.HUMBLE:
    IGNORED_SERVICE_MESSAGE_TYPES.update(NOT_IN_HUMBLE_SERVICE_MESSAGE_TYPES)


def _is_unsupported_message_type(value: Any) -> bool:
    return isinstance(getattr(value, "__unsupported_reason__", None), str)


def _is_core_schema(value: object) -> bool:
    return isinstance(value, dict) and isinstance(value.get("__typename"), str)


def _core_message_schemas_by_typename() -> dict[str, core.CoreSchema]:
    by_typename: dict[str, core.CoreSchema] = {}
    for value in vars(core.all_msgs).values():
        if not _is_core_schema(value):
            continue
        schema = value
        type_name = schema["__typename"]
        if "/msg/" not in type_name:
            continue
        by_typename.setdefault(type_name, schema)
    return by_typename


def _is_message_type(value: Any) -> bool:
    return (
        inspect.isclass(value)
        and issubclass(value, IdlStruct)
        and value is not IdlStruct
    )


def _collect_unsupported_message_typenames(
    namespace: Mapping[str, Any],
) -> set[str]:
    unsupported: set[str] = set()
    for value in namespace.values():
        if not _is_message_type(value):
            continue
        if not _is_unsupported_message_type(value):
            continue
        type_name = value.get_type_name()
        if "/msg/" in type_name:
            unsupported.add(type_name)
    return unsupported


def _collect_unsupported_service_message_typenames(
    namespace: Mapping[str, Any],
) -> set[str]:
    unsupported: set[str] = set()
    for value in namespace.values():
        if not _is_message_type(value):
            continue
        if not _is_unsupported_message_type(value):
            continue
        type_name = value.get_type_name()
        if "/srv/" not in type_name:
            continue
        if not (
            type_name.endswith("_Request")
            or type_name.endswith("_Response")
        ):
            continue
        unsupported.add(type_name)
    return unsupported


def _collect_unique_message_types(
    namespace: Mapping[str, Any],
) -> list[type[IdlStruct]]:
    by_typename: dict[str, type[IdlStruct]] = {}
    for value in namespace.values():
        if not _is_message_type(value):
            continue
        msg_type = value
        type_name = msg_type.get_type_name()
        if "/msg/" not in type_name:
            continue
        by_typename.setdefault(type_name, msg_type)
    return [by_typename[type_name] for type_name in sorted(by_typename)]


def random_message_for_type(
    msg_type: type[IdlStruct], seed: int | None = None
) -> IdlStruct:
    core_schema = msg_type.to_core_schema()
    core_msg = core.random_message(core_schema, seed=seed)
    return msg_type.from_core_message(core_msg)


def _is_service_type(value: Any) -> bool:
    return (
        hasattr(value, "get_type_name")
        and hasattr(value, "Request")
        and hasattr(value, "Response")
        and hasattr(value, "Event")
    )


def _collect_unique_service_types(namespace: Mapping[str, Any]) -> list[type[Any]]:
    by_typename: dict[str, type[Any]] = {}
    for value in namespace.values():
        if not _is_service_type(value):
            continue
        service_type = value
        type_name = service_type.get_type_name()
        if "/srv/" not in type_name:
            continue
        if (
            type_name.endswith("_Request")
            or type_name.endswith("_Response")
            or type_name.endswith("_Event")
        ):
            continue
        by_typename.setdefault(type_name, service_type)
    return [by_typename[type_name] for type_name in sorted(by_typename)]


def _collect_unique_service_message_types(
    namespace: Mapping[str, Any],
) -> list[type[IdlStruct]]:
    by_typename: dict[str, type[IdlStruct]] = {}
    for value in namespace.values():
        if not _is_message_type(value):
            continue
        service_msg_type = value
        type_name = service_msg_type.get_type_name()
        if "/srv/" not in type_name:
            continue
        if not (
            type_name.endswith("_Request")
            or type_name.endswith("_Response")
        ):
            continue
        by_typename.setdefault(type_name, service_msg_type)
    return [by_typename[type_name] for type_name in sorted(by_typename)]


def _skip_for_typename(typename: str, ignored_typenames: set[str]) -> Any:
    if typename in ignored_typenames:
        return [pytest.mark.skip(reason=f"in ignore list: {typename}")]
    return []


IGNORED_MESSAGE_TYPES.update(_collect_unsupported_message_typenames(vars(all_msgs)))
IGNORED_SERVICE_MESSAGE_TYPES.update(
    _collect_unsupported_service_message_typenames(vars(all_srvs))
)


MESSAGE_TYPES: list[type[IdlStruct]] = _collect_unique_message_types(vars(all_msgs))
MESSAGE_TYPE_IDS: list[str] = [msg_type.get_type_name() for msg_type in MESSAGE_TYPES]
MESSAGE_TYPE_PARAMS = [
    pytest.param(
        msg_type,
        id=msg_type.get_type_name(),
        marks=_skip_for_typename(msg_type.get_type_name(), IGNORED_MESSAGE_TYPES),
    )
    for msg_type in MESSAGE_TYPES
]
MESSAGE_VALUES: list[IdlStruct] = [
    random_message_for_type(msg_type) for msg_type in MESSAGE_TYPES
]
MESSAGE_VALUE_IDS: list[str] = [type(msg).get_type_name() for msg in MESSAGE_VALUES]
MESSAGE_VALUE_PARAMS = [
    pytest.param(
        msg,
        id=type(msg).get_type_name(),
        marks=_skip_for_typename(type(msg).get_type_name(), IGNORED_MESSAGE_TYPES),
    )
    for msg in MESSAGE_VALUES
]

SERVICE_TYPES: list[type[Any]] = _collect_unique_service_types(vars(all_srvs))
SERVICE_TYPE_IDS: list[str] = [
    service_type.get_type_name() for service_type in SERVICE_TYPES
]
SERVICE_TYPE_PARAMS = [
    pytest.param(
        service_type,
        id=service_type.get_type_name(),
        marks=_skip_for_typename(service_type.get_type_name(), IGNORED_SERVICE_TYPES),
    )
    for service_type in SERVICE_TYPES
]

SERVICE_MESSAGE_TYPES: list[type[IdlStruct]] = _collect_unique_service_message_types(
    vars(all_srvs)
)
SERVICE_MESSAGE_TYPE_IDS: list[str] = [
    service_msg_type.get_type_name() for service_msg_type in SERVICE_MESSAGE_TYPES
]
SERVICE_MESSAGE_TYPE_PARAMS = [
    pytest.param(
        service_msg_type,
        id=service_msg_type.get_type_name(),
        marks=_skip_for_typename(
            service_msg_type.get_type_name(),
            IGNORED_SERVICE_MESSAGE_TYPES,
        ),
    )
    for service_msg_type in SERVICE_MESSAGE_TYPES
]
SERVICE_MESSAGE_VALUES: list[IdlStruct] = [
    service_msg_type() for service_msg_type in SERVICE_MESSAGE_TYPES
]
SERVICE_MESSAGE_VALUE_IDS: list[str] = [
    type(msg).get_type_name() for msg in SERVICE_MESSAGE_VALUES
]
SERVICE_MESSAGE_VALUE_PARAMS = [
    pytest.param(
        msg,
        id=type(msg).get_type_name(),
        marks=_skip_for_typename(
            type(msg).get_type_name(),
            IGNORED_SERVICE_MESSAGE_TYPES,
        ),
    )
    for msg in SERVICE_MESSAGE_VALUES
]
CORE_MESSAGE_SCHEMAS_BY_TYPENAME = _core_message_schemas_by_typename()
