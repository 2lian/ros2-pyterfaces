from collections.abc import Mapping, Sequence as SequenceABC
from importlib import import_module
from typing import Any

from .schema import get_type_name
from .types import (
    _EVENT_FIELD,
    _REQUEST_FIELD,
    _RESPONSE_FIELD,
    _SERVICE_FIELDS,
    _TYPENAME_KEY,
    Array,
    BoundedString,
    CoreSchema,
    SchemaEntry,
    Sequence,
)


def _sequence_items(value: Any) -> list[Any] | None:
    if isinstance(value, (str, bytes, bytearray, memoryview, Mapping)):
        return None

    if isinstance(value, SequenceABC):
        return list(value)

    tolist = getattr(value, "tolist", None)
    if callable(tolist):
        converted = tolist()
        if isinstance(converted, list):
            return converted
        if isinstance(converted, tuple):
            return list(converted)
        return None

    if hasattr(value, "__iter__") and hasattr(value, "__len__"):
        try:
            return list(value)
        except TypeError:
            return None

    return None


def _is_sequence_like(value: Any) -> bool:
    return _sequence_items(value) is not None


def _is_service_typename(type_name: str) -> bool:
    return "/srv/" in type_name and not (
        type_name.endswith("_Request")
        or type_name.endswith("_Response")
        or type_name.endswith("_Event")
    )


def _is_service_schema(schema: Mapping[str, Any]) -> bool:
    return all(field in schema for field in _SERVICE_FIELDS)


def _get_field_value(obj: Any, field_name: str) -> Any:
    if isinstance(obj, Mapping):
        if field_name not in obj:
            raise AttributeError(f"Missing field {field_name!r} in mapping")
        return obj[field_name]

    if not hasattr(obj, field_name):
        raise AttributeError(
            f"{type(obj).__module__}.{type(obj).__name__} has no field {field_name!r}"
        )

    return getattr(obj, field_name)


def to_ros_type(schema: CoreSchema) -> type:
    type_name = get_type_name(schema)
    if "/" not in type_name:
        raise ValueError(
            f"Invalid ROS type name {type_name!r}. Expected 'pkg/msg/Name' or 'pkg/srv/Name'."
        )

    module_name, class_name = type_name.replace("/", ".").rsplit(".", 1)
    module = import_module(module_name)

    direct = getattr(module, class_name, None)
    if direct is not None:
        return direct

    if class_name.endswith("_Request"):
        service_name = class_name.removesuffix("_Request")
        service = getattr(module, service_name, None)
        if service is not None and hasattr(service, "Request"):
            return service.Request

    if class_name.endswith("_Response"):
        service_name = class_name.removesuffix("_Response")
        service = getattr(module, service_name, None)
        if service is not None and hasattr(service, "Response"):
            return service.Response

    if class_name.endswith("_Event"):
        service_name = class_name.removesuffix("_Event")
        service = getattr(module, service_name, None)
        if service is not None and hasattr(service, "Event"):
            return service.Event

    raise AttributeError(
        f"ROS equivalent for {type_name!r} does not seem to exist in this runtime."
    )


def _from_ros_value(entry: SchemaEntry, value: Any) -> Any:
    if value is None:
        return None

    if isinstance(entry, dict):
        values = _sequence_items(value)
        if values is not None:
            if len(values) == 1:
                return from_ros(entry, values[0])
            return [from_ros(entry, item) for item in values]
        return from_ros(entry, value)

    if isinstance(entry, Sequence):
        if entry.subtype == "byte":
            if isinstance(value, (bytes, bytearray, memoryview)):
                return bytes(value)
            items = _sequence_items(value)
            if items is None:
                raise TypeError(
                    f"Expected a sequence value for {entry!r}, got {value!r}"
                )
            return bytes(
                bytes(item)[0]
                if isinstance(item, (bytes, bytearray, memoryview))
                else int(item)
                for item in items
            )
        items = _sequence_items(value)
        if items is None:
            raise TypeError(f"Expected a sequence value for {entry!r}, got {value!r}")
        return [_from_ros_value(entry.subtype, item) for item in items]

    if isinstance(entry, Array):
        if entry.subtype == "byte":
            if isinstance(value, (bytes, bytearray, memoryview)):
                return bytes(value)
            items = _sequence_items(value)
            if items is None:
                raise TypeError(
                    f"Expected a sequence value for {entry!r}, got {value!r}"
                )
            return bytes(
                bytes(item)[0]
                if isinstance(item, (bytes, bytearray, memoryview))
                else int(item)
                for item in items
            )
        items = _sequence_items(value)
        if items is None:
            if isinstance(value, (bytes, bytearray, memoryview)):
                items = list(bytes(value))
            else:
                raise TypeError(f"Expected a sequence value for {entry!r}, got {value!r}")
        return [_from_ros_value(entry.subtype, item) for item in items]

    if isinstance(entry, BoundedString):
        text = (
            bytes(value).decode("utf-8")
            if isinstance(value, (bytes, bytearray, memoryview))
            else str(value)
        )
        if len(text) > entry.max_length:
            raise ValueError(
                f"String length {len(text)} exceeds bounded length {entry.max_length}"
            )
        return text

    if not isinstance(entry, str):
        raise TypeError(f"Unsupported schema entry: {entry!r}")

    if isinstance(value, (bytes, bytearray, memoryview)):
        if entry == "string":
            return bytes(value).decode("utf-8")
        if entry in {"byte"} and len(bytes(value)) == 1:
            return bytes(value)
        if entry in {"byte", "char", "uint8", "int8"} and len(bytes(value)) == 1:
            return bytes(value)[0]
        return list(bytes(value))

    if entry == "bool":
        return bool(value)
    if entry.startswith("float"):
        return float(value)
    if entry == "string":
        return str(value)
    if entry == "byte":
        return bytes([int(value)])
    return int(value)


def from_ros(schema: CoreSchema, ros_msg: Any) -> dict[str, Any]:
    core_message: dict[str, Any] = {_TYPENAME_KEY: get_type_name(schema)}

    for field_name, entry in schema.items():
        if field_name == _TYPENAME_KEY:
            continue
        ros_value = _get_field_value(ros_msg, field_name)
        core_message[field_name] = _from_ros_value(entry, ros_value)

    return core_message


def _to_ros_value(value: Any, destination_value: Any = None) -> Any:
    if isinstance(value, dict) and _TYPENAME_KEY in value:
        nested = to_ros(value)
        if _is_sequence_like(destination_value):
            return [nested]
        return nested

    if isinstance(value, int) and isinstance(destination_value, bytes):
        return bytes([value])

    if isinstance(value, list):
        return [_to_ros_value(item) for item in value]

    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)

    return value


def to_ros(core_msg: dict[str, Any]) -> Any:
    type_name = get_type_name(core_msg)
    if _is_service_typename(type_name) and _is_service_schema(core_msg):
        return {
            _REQUEST_FIELD: _to_ros_value(core_msg[_REQUEST_FIELD]),
            _RESPONSE_FIELD: _to_ros_value(core_msg[_RESPONSE_FIELD]),
            _EVENT_FIELD: _to_ros_value(core_msg[_EVENT_FIELD]),
        }

    ros_type = to_ros_type(core_msg)
    ros_msg = ros_type()

    for field_name, value in core_msg.items():
        if field_name == _TYPENAME_KEY:
            continue
        if not hasattr(ros_msg, field_name):
            continue

        destination_value = getattr(ros_msg, field_name)
        setattr(ros_msg, field_name, _to_ros_value(value, destination_value))

    return ros_msg
