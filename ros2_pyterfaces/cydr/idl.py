from collections.abc import Mapping
from importlib import import_module
import re
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Protocol,
    Self,
    TypeVar,
    Union,
    cast,
    get_type_hints,
    overload,
)

import msgspec
import numpy as np
from cydr import XcdrStruct as CyStruct
from cydr import types
from cydr.schema_types import _is_ndarray_annotation, _ndarray_fixed_length
from cydr.structs import StringCollectionMode

from .. import core
from ..core import TYPENAME_KEY, CoreSchema, SchemaEntry

_PRIMITIVE_FROM_CYDR: dict[types.PrimitiveSchemaType, core.Primitive] = {
    bool: "bool",  # type: ignore
    np.bool_: "bool",  # type: ignore
    bytes: "string",  # type: ignore
    str: "string",  # type: ignore
    # np.int8: "int8", # shouldn't be used
    # np.uint8: "uint8",
    # np.int16: "int16",
    # np.uint16: "uint16",
    # np.int32: "int32",
    # np.uint32: "uint32",
    # np.int64: "int64",
    # np.uint64: "uint64",
    # np.float32: "float32",
    # np.float64: "float64",
    types.boolean: "bool",
    types.byte: "byte",
    types.int8: "int8",
    types.uint8: "uint8",
    types.int16: "int16",
    types.uint16: "uint16",
    types.int32: "int32",
    types.uint32: "uint32",
    types.int64: "int64",
    types.uint64: "uint64",
    types.float32: "float32",
    types.float64: "float64",
    types.string: "string",
}

_CYDR_COLLEC_BY_PRIMITIVE: dict[core.Primitive, types.PrimitiveSchemaType] = {
    "bool": types.boolean,
    "char": types.uint8,
    "byte": types.byte,
    "int8": types.int8,
    "uint8": types.uint8,
    "int16": types.int16,
    "uint16": types.uint16,
    "int32": types.int32,
    "uint32": types.uint32,
    "int64": types.int64,
    "uint64": types.uint64,
    "float32": types.float32,
    "float64": types.float64,
}


_PRIMITIVE_FROM_CYDR_TOKEN: dict[str, core.Primitive] = {
    "bool": "bool",
    "bytes": "string",
    "str": "string",
    "types.boolean": "bool",
    "types.Bool": "bool",
    "types.byte": "byte",
    "types.int8": "int8",
    "types.Int8": "int8",
    "types.uint8": "uint8",
    "types.UInt8": "uint8",
    "types.int16": "int16",
    "types.Int16": "int16",
    "types.uint16": "uint16",
    "types.UInt16": "uint16",
    "types.int32": "int32",
    "types.Int32": "int32",
    "types.uint32": "uint32",
    "types.UInt32": "uint32",
    "types.int64": "int64",
    "types.Int64": "int64",
    "types.uint64": "uint64",
    "types.UInt64": "uint64",
    "types.float32": "float32",
    "types.Float32": "float32",
    "types.float64": "float64",
    "types.Float64": "float64",
    "types.string": "string",
    "types.Bytes": "string",
}

_FIXED_SHAPE_RE = re.compile(r"""types\.Shape\[(?:"|')(\d+)(?:"|')\]""")


def _schema_field_annotations(cls: type[CyStruct]) -> dict[str, Any]:
    raw = getattr(cls, "__annotations__", {})
    if not isinstance(raw, dict):
        return {}
    return {field_name: raw[field_name] for field_name in cls.__struct_fields__}


def _value_field_annotations(cls: type) -> dict[str, Any]:
    hints = get_type_hints(cls, include_extras=True)
    return {field_name: hints[field_name] for field_name in cls.__struct_fields__}


def _type_from_forward_ref(annotation: str, owner_cls: type[CyStruct]) -> Any:
    module = import_module(owner_cls.__module__)
    return eval(annotation, vars(module))


def _primitive_from_token(token: str) -> core.Primitive | None:
    return _PRIMITIVE_FROM_CYDR_TOKEN.get(token.strip())


def _schema_entry_from_annotation(
    annotation: Any, *, owner_cls: type[CyStruct]
) -> SchemaEntry:
    if isinstance(annotation, str):
        primitive = _primitive_from_token(annotation)
        if primitive is not None:
            return primitive

        if annotation.startswith("types.NDArray[") and annotation.endswith("]"):
            inner = annotation[len("types.NDArray[") : -1]
            shape_token, element_token = [part.strip() for part in inner.split(",", 1)]
            element_primitive = _primitive_from_token(element_token)
            if element_primitive is None:
                raise ValueError(
                    f"Collection annotation with unsupported element token {element_token!r}"
                )
            if shape_token == "Any":
                return core.Sequence(element_primitive)
            fixed_match = _FIXED_SHAPE_RE.fullmatch(shape_token)
            if fixed_match is not None:
                return core.Array(element_primitive, int(fixed_match.group(1)))
            raise ValueError(
                f"Collection annotation with unsupported shape token {shape_token!r}"
            )

        resolved = _type_from_forward_ref(annotation, owner_cls)
        if isinstance(resolved, type) and issubclass(resolved, IdlStruct):
            return resolved.to_core_schema()

        primitive_from_ref = _PRIMITIVE_FROM_CYDR.get(resolved)
        if primitive_from_ref is None:
            raise ValueError(
                f"Unsupported cydr annotation {annotation!r} resolved as {resolved!r}"
            )
        return primitive_from_ref

    if isinstance(annotation, type) and issubclass(annotation, IdlStruct):
        return annotation.to_core_schema()

    if _is_ndarray_annotation(annotation):
        _, arr_dtype = annotation.__args__
        primitive = _PRIMITIVE_FROM_CYDR.get(arr_dtype)
        if primitive is None:
            raise ValueError(
                f"Collection annotation with {arr_dtype=} not supported by cydr"
            )
        length = _ndarray_fixed_length(annotation)
        if length is None:
            return core.Sequence(primitive)
        return core.Array(primitive, length)

    return _PRIMITIVE_FROM_CYDR[annotation]


def _scalar_to_core(primitive: str, value: Any) -> Any:
    if primitive == "bool":
        if not isinstance(value, (bool, np.bool_)):
            raise ValueError(f"Expected cydr value for bool to be bool, got {value=}")
        return bool(value)
    if primitive in {"float32", "float64"}:
        if not isinstance(value, (float, np.floating)):
            raise ValueError(
                f"Expected cydr value for {primitive} to be float, got {value=}"
            )
        return float(value)
    if primitive == "string":
        if isinstance(value, (bytes, bytearray, memoryview)):
            return bytes(value).decode("utf-8")
        if isinstance(value, str):
            return value
        raise ValueError(
            "Expected cydr value for string to be "
            f"(bytes | bytearray | memoryview | str), got {value=}"
        )
    if primitive == "byte":
        if isinstance(value, (bytes, bytearray, memoryview)):
            if len(value) == 1:
                return bytes(value)
            raise ValueError(
                "Expected cydr value for byte to be "
                "(bytes | bytearray | memoryview) with len == 1, "
                f"got {value=}"
            )
        if isinstance(value, (int, np.integer)) and not isinstance(value, bool):
            return bytes([int(value)])
        raise ValueError(
            "Expected cydr value for byte to be "
            "(bytes | bytearray | memoryview) with len == 1 or integer, "
            f"got {value=}"
        )
    if not isinstance(value, (int, np.integer)) or isinstance(value, bool):
        raise ValueError(
            f"Expected cydr value for {primitive} to be integer, got {value=}"
        )
    return int(value)


def _scalar_from_core(primitive: core.Primitive, value: Any) -> Any:
    if primitive == "string":
        if not isinstance(value, str):
            raise ValueError(
                f"Expected core representation of string to be str, got {value=}"
            )
        return value.encode("utf-8")
    if primitive == "byte":
        if isinstance(value, (bytes, bytearray, memoryview)):
            if len(value) == 1:
                return np.uint8(bytes(value)[0])
        raise ValueError(
            "Expected core representation of byte to be "
            "(bytes | bytearray | memoryview) with len == 1, "
            f"got {value=}"
        )
    if primitive == "bool":
        if not isinstance(value, bool):
            raise ValueError(
                f"Expected core representation of bool to be bool, got {value=}"
            )
        return np.bool_(value)
    if primitive in {"float32", "float64"}:
        if not isinstance(value, float):
            raise ValueError(
                f"Expected core representation of {primitive} to be float, got {value=}"
            )
        return _CYDR_COLLEC_BY_PRIMITIVE[primitive](value)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(
            f"Expected core representation of {primitive} to be int, got {value=}"
        )
    return _CYDR_COLLEC_BY_PRIMITIVE[primitive](value)


def _value_to_core(schema_entry: SchemaEntry, value: Any) -> Any:
    if isinstance(schema_entry, dict):
        return value.to_core_message()

    if isinstance(schema_entry, (core.Sequence, core.Array)):
        subtype = schema_entry.subtype
        if isinstance(subtype, dict):
            raise NotImplementedError("cydr does not support collection of struct")
        if not isinstance(subtype, str):
            raise NotImplementedError(f"Unsupported cydr collection subtype {subtype}")
        if subtype == "byte":
            if isinstance(value, np.ndarray):
                return value.tobytes()
            raise ValueError(
                "Expected cydr value for byte collection to be "
                "numpy.ndarray, "
                f"got {value=}"
            )
        if subtype == "string":
            if not isinstance(value, np.ndarray):
                raise ValueError(
                    "Expected cydr value for string collection to be numpy.ndarray, "
                    f"got {value=}"
                )
            items = [bytes(item).decode("utf-8") for item in value]
            return items
        if isinstance(value, (bytes, bytearray, memoryview)):
            raise ValueError(
                f"Expected cydr value for {subtype} collection to not be "
                "(bytes | bytearray | memoryview)"
            )
        if not isinstance(value, np.ndarray):
            raise ValueError(
                f"Expected cydr value for {subtype} collection to be numpy.ndarray, "
                f"got {value=}"
            )
        items = [_scalar_to_core(subtype, item) for item in value.tolist()]
        if isinstance(schema_entry, core.Array) and len(items) != schema_entry.length:
            raise ValueError(
                f"Expected cydr value for {subtype} array to have length "
                f"{schema_entry.length}, got {len(items)}"
            )
        return items

    if isinstance(schema_entry, core.BoundedString):
        if isinstance(value, (bytes, bytearray, memoryview)):
            return bytes(value).decode("utf-8")
        if isinstance(value, str):
            return value
        raise ValueError(
            "Expected cydr value for bounded string to be "
            f"(bytes | bytearray | memoryview | str), got {value=}"
        )

    return _scalar_to_core(schema_entry, value)


def _value_from_core(schema_entry: SchemaEntry, value: Any, annotation: Any) -> Any:
    if isinstance(schema_entry, dict):
        if not (isinstance(annotation, type) and issubclass(annotation, IdlStruct)):
            raise ValueError(
                "Expected annotation for nested core struct to be IdlStruct subtype, "
                f"got {annotation=}"
            )
        nested_type = annotation
        return nested_type.from_core_message(cast(Mapping[str, Any], value))

    if isinstance(schema_entry, (core.Sequence, core.Array)):
        subtype = schema_entry.subtype
        if isinstance(subtype, dict):
            raise NotImplementedError("cydr does not support collection of struct")
        if not _is_ndarray_annotation(annotation):
            raise NotImplementedError(
                "cydr collection conversion requires NDArray annotation"
            )
        if not isinstance(subtype, str):
            raise NotImplementedError(f"Unsupported cydr collection subtype {subtype}")
        if subtype == "byte":
            if isinstance(value, (bytes, bytearray, memoryview)):
                raw = np.frombuffer(value, dtype=_CYDR_COLLEC_BY_PRIMITIVE["byte"])
                if (
                    isinstance(schema_entry, core.Array)
                    and len(raw) != schema_entry.length
                ):
                    raise ValueError(
                        "Expected core representation of byte array to have length "
                        f"{schema_entry.length}, got {len(raw)}"
                    )
                return raw
            raise ValueError(
                "Expected core representation of byte collection to be "
                "(bytes | bytearray | memoryview), "
                f"got {value=}"
            )
        if not isinstance(value, list):
            raise ValueError(
                f"Expected core representation of {subtype} collection to be list, "
                f"got {value=}"
            )
        if subtype == "string":
            raw = np.asarray([item.encode("utf-8") for item in value], dtype=np.bytes_)
        else:
            raw = np.asarray(value, dtype=_CYDR_COLLEC_BY_PRIMITIVE[subtype])
        if isinstance(schema_entry, core.Array) and len(raw) != schema_entry.length:
            raise ValueError(
                f"Expected core representation of {subtype} array to have length "
                f"{schema_entry.length}, got {len(raw)}"
            )
        return raw

    if isinstance(schema_entry, core.BoundedString):
        if not isinstance(value, str):
            raise ValueError(
                "Expected core representation of bounded string to be str, "
                f"got {value=}"
            )
        return value.encode("utf-8")

    return _scalar_from_core(schema_entry, value)


class IdlStruct(CyStruct):
    __idl_typename__: ClassVar[str] = ""
    __is_empty_message__: ClassVar[bool] = True

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        raw_annotations = getattr(cls, "__annotations__", None)
        if isinstance(raw_annotations, dict):
            cls.__is_empty_message__ = len(raw_annotations) == 0
        else:
            cls.__is_empty_message__ = True

    def serialize(self) -> bytearray:
        if type(self).__is_empty_message__:
            return DummyEmpty().serialize()
        return super().serialize()

    @classmethod
    def deserialize(
        cls,
        data: Union[bytes, bytearray, memoryview],
        string_collections: Optional[StringCollectionMode] = None,
    ) -> Self:
        if cls.__is_empty_message__:
            DummyEmpty.deserialize(
                data=data,
                string_collections=string_collections,
            )
            return cls()
        return super().deserialize(
            data=data,
            string_collections=string_collections,
        )

    @classmethod
    def to_core_schema(cls) -> CoreSchema:
        schema: CoreSchema = {TYPENAME_KEY: cls.get_type_name()}
        annotations = _schema_field_annotations(cls)
        for field_name in cls.__struct_fields__:
            schema[field_name] = _schema_entry_from_annotation(
                annotations[field_name], owner_cls=cls
            )
        return schema

    @classmethod
    def from_core_schema(cls) -> CoreSchema:
        raise NotImplementedError(
            "cydr does not implement from_core_schema; schema is annotation-driven"
        )

    def to_core_message(self) -> dict[str, Any]:
        schema = type(self).to_core_schema()
        message: dict[str, Any] = {TYPENAME_KEY: type(self).get_type_name()}
        for field_name in self.__struct_fields__:
            message[field_name] = _value_to_core(
                schema[field_name], getattr(self, field_name)
            )
        return message

    @classmethod
    def from_core_message(cls, core_msg: Mapping[str, Any]) -> Self:
        schema = cls.to_core_schema()
        annotations = _value_field_annotations(cls)
        kwargs: dict[str, Any] = {}
        for field_name in cls.__struct_fields__:
            kwargs[field_name] = _value_from_core(
                schema[field_name],
                core_msg[field_name],
                annotations[field_name],
            )
        return cls(**kwargs)

    @classmethod
    def json_type_description(cls, indent: int = 2) -> str:
        return core.json_type_description(cls.to_core_schema(), indent=indent)

    @classmethod
    def _hash_rihs01_raw(cls) -> Any:
        return core._hash_rihs01_raw(cls.to_core_schema())

    @classmethod
    def hash_rihs01(cls) -> str:
        return core.hash_rihs01(cls.to_core_schema())

    @classmethod
    def get_type_name(cls) -> str:
        return cls.__idl_typename__

    @classmethod
    def to_ros_type(cls) -> type:
        return core.to_ros_type(cls.to_core_schema())

    def to_ros(self) -> object:
        return core.to_ros(self.to_core_message())

    @classmethod
    def from_ros(cls, msg: object) -> Self:
        core_msg = core.from_ros(cls.to_core_schema(), msg)
        return cls.from_core_message(core_msg)


JitStruct = IdlStruct


class DummyEmpty(IdlStruct):
    __idl_typename__ = "does/not/matter/empty"
    structure_needs_at_least_one_member: types.uint8 = np.uint8(0)


class Time(IdlStruct):
    __idl_typename__ = "builtin_interfaces/msg/Time"
    sec: types.int32 = np.int32(0)
    nanosec: types.uint32 = np.uint32(0)


class ServiceEventInfo(IdlStruct):
    __idl_typename__ = "service_msgs/msg/ServiceEventInfo"
    REQUEST_SENT: ClassVar[Literal[0]] = 0
    REQUEST_RECEIVED: ClassVar[Literal[1]] = 1
    RESPONSE_SENT: ClassVar[Literal[2]] = 2
    RESPONSE_RECEIVED: ClassVar[Literal[3]] = 3

    event_type: types.uint8 = np.uint8(0)
    stamp: Time = msgspec.field(default_factory=Time)
    client_gid: types.NDArray[types.Shape["16"], types.UInt8] = msgspec.field(
        default_factory=lambda: np.array([0] * 16, dtype=np.uint8)
    )
    sequence_number: types.int64 = np.int64(0)


RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")
EventT = TypeVar("EventT")


class IdlServiceType(Protocol[RequestT, ResponseT, EventT]):
    Request: type[RequestT]
    Response: type[ResponseT]
    Event: type[EventT]

    @classmethod
    def get_type_name(cls) -> str: ...

    @classmethod
    def to_core_schema(cls) -> CoreSchema: ...

    @classmethod
    def json_type_description(cls, indent: int = 2) -> str: ...

    @classmethod
    def _hash_rihs01_raw(cls) -> Any: ...

    @classmethod
    def hash_rihs01(cls) -> str: ...

    @classmethod
    def to_ros_type(cls) -> type: ...


def _service_name_from_request_response(
    request: type[IdlStruct], response: type[IdlStruct]
) -> str:
    return core._service_name_from_request_response(
        request.get_type_name(),
        response.get_type_name(),
    )


def _make_service_event_type(
    request: type[IdlStruct],
    response: type[IdlStruct],
    service_type_name: str,
    module_name: str,
) -> type:
    event_type_name = f"{service_type_name}_Event"
    event_class_name = event_type_name.rsplit("/", 1)[-1]
    event_core_schema = core.make_srv_schema(
        request.to_core_schema(),
        response.to_core_schema(),
        typename=service_type_name,
    )["event_message"]

    @classmethod
    def get_type_name(cls) -> str:
        return cast(str, cls.__idl_typename__)

    @classmethod
    def to_core_schema(cls) -> CoreSchema:
        return event_core_schema

    @classmethod
    def json_type_description(cls, indent: int = 2) -> str:
        return core.json_type_description(cls.to_core_schema(), indent=indent)

    @classmethod
    def _hash_rihs01_raw(cls) -> Any:
        return core._hash_rihs01_raw(cls.to_core_schema())

    @classmethod
    def hash_rihs01(cls) -> str:
        return core.hash_rihs01(cls.to_core_schema())

    @classmethod
    def to_ros_type(cls) -> type:
        return core.to_ros_type(cls.to_core_schema())

    def serialize(self) -> bytearray:
        raise NotImplementedError(
            "cydr service event placeholder does not implement serialize"
        )

    @classmethod
    def deserialize(
        cls,
        data: Union[bytes, bytearray, memoryview],
        string_collections: Optional[StringCollectionMode] = None,
    ) -> Any:
        raise NotImplementedError(
            "cydr service event placeholder does not implement deserialize"
        )

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} is a service event type "
            "placeholder and cannot be instantiated"
        )

    namespace = {
        "__module__": module_name,
        "__idl_typename__": event_type_name,
        "__unsupported_reason__": (
            "auto-generated service events are represented as core schema only "
            "for cydr service metadata and hashes"
        ),
        "__new__": __new__,
        "get_type_name": get_type_name,
        "to_core_schema": to_core_schema,
        "json_type_description": json_type_description,
        "_hash_rihs01_raw": _hash_rihs01_raw,
        "hash_rihs01": hash_rihs01,
        "to_ros_type": to_ros_type,
        "serialize": serialize,
        "deserialize": deserialize,
    }
    return cast(type, type(event_class_name, (), namespace))


def _make_service_type(
    request: type[IdlStruct],
    response: type[IdlStruct],
    event_type: type,
    service_type_name: str,
    module_name: str,
) -> type:
    class_name = service_type_name.rsplit("/", 1)[-1]

    @classmethod
    def get_type_name(cls) -> str:
        return cast(str, cls.__idl_typename__)

    @classmethod
    def to_core_schema(cls) -> CoreSchema:
        return core.make_srv_schema(
            request.to_core_schema(),
            response.to_core_schema(),
            typename=cls.get_type_name(),
        )

    @classmethod
    def json_type_description(cls, indent: int = 2) -> str:
        return core.json_type_description(cls.to_core_schema(), indent=indent)

    @classmethod
    def _hash_rihs01_raw(cls) -> Any:
        return core._hash_rihs01_raw(cls.to_core_schema())

    @classmethod
    def hash_rihs01(cls) -> str:
        return core.hash_rihs01(cls.to_core_schema())

    @classmethod
    def to_ros_type(cls) -> type:
        return core.to_ros_type(cls.to_core_schema())

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} is a service type and cannot be instantiated"
        )

    namespace = {
        "__module__": module_name,
        "__idl_typename__": service_type_name,
        "Request": request,
        "Response": response,
        "Event": event_type,
        "__new__": __new__,
        "get_type_name": get_type_name,
        "to_core_schema": to_core_schema,
        "json_type_description": json_type_description,
        "_hash_rihs01_raw": _hash_rihs01_raw,
        "hash_rihs01": hash_rihs01,
        "to_ros_type": to_ros_type,
    }
    return cast(type, type(class_name, (), namespace))


@overload
def make_idl_service(
    request: type[RequestT],
    response: type[ResponseT],
    _event_type: type[EventT],
    typename: str | None = None,
    _module_name: str | None = None,
) -> IdlServiceType[RequestT, ResponseT, EventT]: ...


@overload
def make_idl_service(
    request: type[RequestT],
    response: type[ResponseT],
    _event_type: None = None,
    typename: str | None = None,
    _module_name: str | None = None,
) -> IdlServiceType[RequestT, ResponseT, IdlStruct]: ...


def make_idl_service(
    request: type[RequestT],
    response: type[ResponseT],
    _event_type: type[EventT] | None = None,
    typename: str | None = None,
    _module_name: str | None = None,
) -> IdlServiceType[RequestT, ResponseT, Any]:
    service_type_name = (
        typename
        if typename is not None
        else _service_name_from_request_response(
            cast(type[IdlStruct], request),
            cast(type[IdlStruct], response),
        )
    )
    module_name = _module_name if _module_name is not None else request.__module__
    event_type = (
        cast(type[IdlStruct], _event_type)
        if _event_type is not None
        else _make_service_event_type(
            cast(type[IdlStruct], request),
            cast(type[IdlStruct], response),
            service_type_name,
            module_name,
        )
    )
    return cast(
        IdlServiceType[RequestT, ResponseT, Any],
        _make_service_type(
            cast(type[IdlStruct], request),
            cast(type[IdlStruct], response),
            event_type,
            service_type_name,
            module_name,
        ),
    )
