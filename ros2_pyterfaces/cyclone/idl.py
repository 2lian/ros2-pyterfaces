from collections.abc import Mapping as MappingABC
from collections.abc import Sequence as SequenceABC
from dataclasses import dataclass, field, fields
from typing import (
    Annotated,
    Any,
    ClassVar,
    Final,
    Literal,
    Mapping,
    Protocol,
    Self,
    TypeVar,
    cast,
    get_args,
    get_origin,
    get_type_hints,
    overload,
)

import cyclonedds_idl as _idl
from cyclonedds_idl import types

from .. import core
from ..core import PRIMITIVES, TYPENAME_KEY, CoreSchema, Primitive, SchemaEntry


def _unwrap_annotated(annotation: Any) -> tuple[Any, tuple[Any, ...]]:
    metadata: list[Any] = []
    base = annotation
    while get_origin(base) is Annotated:
        args = get_args(base)
        if not args:
            break
        base = args[0]
        metadata.extend(args[1:])
    return base, tuple(metadata)


def _is_ignored_annotation(annotation: Any) -> bool:
    base, _ = _unwrap_annotated(annotation)
    origin = get_origin(base)
    if origin in {ClassVar, Final}:
        return True

    if isinstance(annotation, str):
        normalized = annotation.replace("typing.", "")
        if "ClassVar[" in normalized or normalized.startswith("ClassVar"):
            return True
        if "Final[" in normalized or normalized.startswith("Final"):
            return True

    return False


def _strip_ignored_annotations(namespace: dict[str, Any]) -> None:
    raw = namespace.get("__annotations__")
    if not isinstance(raw, dict):
        return

    namespace["__annotations__"] = {
        name: annotation
        for name, annotation in raw.items()
        if not name.startswith("__") and not _is_ignored_annotation(annotation)
    }


def _field_annotations(cls: type) -> dict[str, Any]:
    hints = get_type_hints(cls, include_extras=True)
    annotations: dict[str, Any] = {}

    for dataclass_field in fields(cls):
        name = dataclass_field.name
        annotation = hints[name]
        if _is_ignored_annotation(annotation):
            continue
        annotations[name] = annotation

    return annotations


def _primitive_from_base(base: Any) -> Primitive:
    if base is bool:
        return "bool"
    if base is str:
        return "string"
    if base is float:
        return "float64"
    if base is int:
        return "int64"
    raise TypeError(f"Unsupported primitive annotation base: {base!r}")


def _primitive_from_annotation(annotation: Any) -> Primitive:
    base, metadata = _unwrap_annotated(annotation)
    for meta in metadata:
        if isinstance(meta, str) and meta in PRIMITIVES:
            return cast(Primitive, meta)
    if isinstance(base, type):
        return _primitive_from_base(base)
    raise TypeError(f"Unsupported primitive annotation: {annotation!r}")


def _sequence_subtype(annotation: Any) -> Any | None:
    base, metadata = _unwrap_annotated(annotation)

    for meta in metadata:
        subtype = getattr(meta, "subtype", None)
        if subtype is not None:
            return subtype

    origin = get_origin(base)
    if origin in {list, tuple, SequenceABC}:
        args = get_args(base)
        if args:
            return args[0]
    return None


def _schema_entry_from_annotation(annotation: Any) -> SchemaEntry:
    base, metadata = _unwrap_annotated(annotation)

    for meta in metadata:
        if isinstance(meta, str) and meta in PRIMITIVES:
            return cast(Primitive, meta)

        subtype = getattr(meta, "subtype", None)
        length = getattr(meta, "length", None)
        max_length = getattr(meta, "max_length", None)

        if subtype is not None and length is not None:
            return core.Array(_schema_entry_from_annotation(subtype), int(length))
        if subtype is not None:
            sequence_max_length: int | None = None
            if max_length is not None:
                sequence_max_length = int(max_length)
            return core.Sequence(
                _schema_entry_from_annotation(subtype),
                sequence_max_length,
            )
        if max_length is not None:
            return core.BoundedString(int(max_length))

    if isinstance(base, type) and issubclass(base, IdlStruct):
        return base.to_core_schema()

    subtype = _sequence_subtype(annotation)
    if subtype is not None:
        return core.Sequence(_schema_entry_from_annotation(subtype))

    if isinstance(base, type):
        return _primitive_from_base(base)

    raise TypeError(f"Unsupported annotation: {annotation!r}")


def _sequence_items(value: Any) -> list[Any] | None:
    if isinstance(value, (str, bytes, bytearray, memoryview, MappingABC)):
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

    if hasattr(value, "__iter__") and hasattr(value, "__len__"):
        try:
            return list(value)
        except TypeError:
            return None

    return None


def _value_from_core(annotation: Any, value: Any) -> Any:
    if value is None:
        return None

    base, _ = _unwrap_annotated(annotation)

    if isinstance(base, type) and issubclass(base, IdlStruct):
        if isinstance(value, MappingABC):
            return base.from_core_message(cast(Mapping[str, Any], value))
        return value

    subtype = _sequence_subtype(annotation)
    if subtype is not None:
        items = _sequence_items(value)
        if items is None:
            if isinstance(value, (bytes, bytearray, memoryview)):
                items = list(bytes(value))
            elif isinstance(value, MappingABC):
                items = [value]
            else:
                raise TypeError(
                    f"Expected sequence value for {annotation!r}, got {value!r}"
                )
        return [_value_from_core(subtype, item) for item in items]

    primitive = _primitive_from_annotation(annotation)
    if primitive == "bool":
        return bool(value)
    if primitive in {"float32", "float64"}:
        return float(value)
    if primitive == "string":
        if isinstance(value, (bytes, bytearray, memoryview)):
            return bytes(value).decode("utf-8")
        return str(value)
    if primitive == "byte":
        if isinstance(value, (bytes, bytearray, memoryview)):
            raw = bytes(value)
            if len(raw) != 1:
                raise TypeError(
                    f"Expected single-byte value for {annotation!r}, got {value!r}"
                )
            return raw[0]
        return int(value)
    if primitive in {"char", "uint8", "int8"} and isinstance(
        value, (bytes, bytearray, memoryview)
    ):
        raw = bytes(value)
        if len(raw) == 1:
            return raw[0]
        return list(raw)
    return int(value)

    return value


def _value_to_core(annotation: Any, value: Any) -> Any:
    if value is None:
        return None

    base, _ = _unwrap_annotated(annotation)

    if isinstance(base, type) and issubclass(base, IdlStruct):
        return value.to_core_message()

    subtype = _sequence_subtype(annotation)
    if subtype is not None:
        return [_value_to_core(subtype, item) for item in value]

    primitive = _primitive_from_annotation(annotation)
    if primitive == "bool":
        return bool(value)
    if primitive in {"float32", "float64"}:
        return float(value)
    if primitive == "string":
        if isinstance(value, (bytes, bytearray, memoryview)):
            return bytes(value).decode("utf-8")
        return str(value)
    if primitive == "byte":
        if isinstance(value, (bytes, bytearray, memoryview)):
            raw = bytes(value)
            if len(raw) == 1:
                return raw
            raise TypeError(
                f"Expected single-byte value for {annotation!r}, got {value!r}"
            )
        as_int = int(value)
        if as_int < 0 or as_int > 255:
            raise ValueError(f"Byte value out of range: {as_int}")
        return bytes([as_int])
    if primitive in {"char", "uint8", "int8"} and isinstance(
        value, (bytes, bytearray, memoryview)
    ):
        raw = bytes(value)
        if len(raw) == 1:
            return raw[0]
        return list(raw)
    return int(value)


class IdlMetaIgnoreFinal(type(_idl.IdlStruct)):
    def __new__(mcls, name, bases, namespace, **kwargs):
        typename = kwargs.pop("typename", None)
        if typename is not None:
            namespace["__idl_typename__"] = typename
        _strip_ignored_annotations(namespace)
        return super().__new__(mcls, name, bases, namespace, **kwargs)


class IdlStruct(_idl.IdlStruct, metaclass=IdlMetaIgnoreFinal):
    __idl_typename__: ClassVar[str] = ""
    __is_empty_message__: ClassVar[bool] = True

    def __init_subclass__(cls, typename: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if typename is not None:
            cls.__idl_typename__ = typename
        raw_annotations = getattr(cls, "__annotations__", None)
        if isinstance(raw_annotations, dict):
            cls.__is_empty_message__ = len(raw_annotations) == 0
        else:
            cls.__is_empty_message__ = True

    def serialize(
        self,
        buffer: _idl.Buffer | None = None,
        endianness: _idl.Endianness | None = None,
        use_version_2: bool | None = None,
    ) -> bytes:
        if type(self).__is_empty_message__:
            return DummyEmpty().serialize(
                buffer=buffer,
                endianness=endianness,
                use_version_2=use_version_2,
            )
        return super().serialize(
            buffer=buffer,
            endianness=endianness,
            use_version_2=use_version_2,
        )

    @classmethod
    def deserialize(
        cls,
        data: bytes,
        has_header: bool = True,
        use_version_2: bool | None = None,
    ) -> Self:
        if cls.__is_empty_message__:
            DummyEmpty.deserialize(
                data,
                has_header=has_header,
                use_version_2=use_version_2,
            )
            return cls()
        return cast(
            Self,
            super().deserialize(
                data,
                has_header=has_header,
                use_version_2=use_version_2,
            ),
        )

    @classmethod
    def to_core_schema(cls) -> CoreSchema:
        schema: CoreSchema = {TYPENAME_KEY: cls.get_type_name()}
        annotations = _field_annotations(cls)
        for dataclass_field in fields(cls):
            name = dataclass_field.name
            schema[name] = _schema_entry_from_annotation(annotations[name])
        return schema

    @classmethod
    def from_core_schema(cls) -> CoreSchema:
        return cls.to_core_schema()

    def to_core_message(self) -> dict[str, Any]:
        cls = type(self)
        annotations = _field_annotations(cls)
        message: dict[str, Any] = {TYPENAME_KEY: cls.get_type_name()}
        for dataclass_field in fields(cls):
            name = dataclass_field.name
            message[name] = _value_to_core(annotations[name], getattr(self, name))
        return message

    @classmethod
    def from_core_message(cls, core_msg: Mapping[str, Any]) -> Self:
        annotations = _field_annotations(cls)
        kwargs: dict[str, Any] = {}
        for dataclass_field in fields(cls):
            name = dataclass_field.name
            if name not in core_msg:
                continue
            kwargs[name] = _value_from_core(annotations[name], core_msg[name])
        return cls(**kwargs)

    @classmethod
    def json_type_description(
        cls,
        root_type_name: str | None = None,
        type_name_overrides: Mapping[type, str] | None = None,
        indent: int = 2,
    ) -> str:
        if root_type_name is not None:
            raise ValueError(
                "root_type_name is not supported in cyclone core-backed mode"
            )
        if type_name_overrides is not None:
            raise ValueError(
                "type_name_overrides is not supported in cyclone core-backed mode"
            )
        return core.json_type_description(cls.to_core_schema(), indent=indent)

    @classmethod
    def _hash_rihs01_raw(cls) -> Any:
        return core._hash_rihs01_raw(cls.to_core_schema())

    @classmethod
    def hash_rihs01(cls) -> str:
        return core.hash_rihs01(cls.to_core_schema())

    @classmethod
    def get_type_name(cls) -> str:
        type_name = cls.__idl_typename__
        if not isinstance(type_name, str) or not type_name:
            raise ValueError(
                f"{cls.__module__}.{cls.__qualname__} is missing a non-empty __idl_typename__"
            )
        return type_name

    @classmethod
    def to_ros_type(cls) -> type:
        return core.to_ros_type(cls.to_core_schema())

    def to_ros(self) -> object:
        return core.to_ros(self.to_core_message())

    @classmethod
    def from_ros(cls, msg: object) -> Self:
        core_msg = core.from_ros(cls.to_core_schema(), msg)
        return cls.from_core_message(core_msg)


@dataclass
class DummyEmpty(IdlStruct, typename="does/not/matter/empty"):
    structure_needs_at_least_one_member: types.uint8 = 0


@dataclass
class Time(IdlStruct, typename="builtin_interfaces/msg/Time"):
    sec: types.int32 = 0
    nanosec: types.uint32 = 0


@dataclass
class ServiceEventInfo(IdlStruct, typename="service_msgs/msg/ServiceEventInfo"):
    REQUEST_SENT: ClassVar[Literal[0]] = 0
    REQUEST_RECEIVED: ClassVar[Literal[1]] = 1
    RESPONSE_SENT: ClassVar[Literal[2]] = 2
    RESPONSE_RECEIVED: ClassVar[Literal[3]] = 3

    event_type: types.uint8 = 0
    stamp: Time = field(default_factory=Time)
    client_gid: types.array[types.uint8, 16] = field(default_factory=lambda: [0] * 16)
    sequence_number: types.int64 = 0


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


def _service_name_from_request_response(  # we should recycle the core here instead of duplicating.
    request: type[IdlStruct], response: type[IdlStruct]
) -> str:
    return core._service_name_from_request_response(
        request.get_type_name(), response.get_type_name()
    )


def _make_service_event_type(
    request: type[IdlStruct],
    response: type[IdlStruct],
    service_type_name: str,
    module_name: str,
) -> type[IdlStruct]:
    event_class_name = f"{service_type_name.rsplit('/', 1)[-1]}_Event"
    event_type_name = f"{service_type_name}_Event"

    namespace: dict[str, Any] = {
        "__module__": module_name,
        "__idl_typename__": event_type_name,
        "__annotations__": {
            "info": ServiceEventInfo,
            "request": types.sequence[request, 1],
            "response": types.sequence[response, 1],
        },
        "info": field(default_factory=ServiceEventInfo),
        "request": field(default_factory=list),
        "response": field(default_factory=list),
    }
    event_type = cast(
        type[IdlStruct], IdlMetaIgnoreFinal(event_class_name, (IdlStruct,), namespace)
    )
    return dataclass(event_type)


def _make_service_type(
    request: type[IdlStruct],
    response: type[IdlStruct],
    event_type: type[IdlStruct],
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
    if not issubclass(request, IdlStruct):
        raise TypeError(f"request must be an IdlStruct type, got {request!r}")
    if not issubclass(response, IdlStruct):
        raise TypeError(f"response must be an IdlStruct type, got {response!r}")
    if _event_type is not None and not issubclass(_event_type, IdlStruct):
        raise TypeError(f"_event_type must be an IdlStruct type, got {_event_type!r}")

    if typename is not None:
        service_type_name = typename
    else:
        service_type_name = _service_name_from_request_response(
            cast(type[IdlStruct], request),
            cast(type[IdlStruct], response),
        )

    if _module_name is not None:
        module_name = _module_name
    else:
        module_name = request.__module__

    if _event_type is not None:
        resolved_event_type: type[IdlStruct] = cast(type[IdlStruct], _event_type)
    else:
        resolved_event_type = _make_service_event_type(
            cast(type[IdlStruct], request),
            cast(type[IdlStruct], response),
            service_type_name,
            module_name,
        )

    return cast(
        IdlServiceType[RequestT, ResponseT, Any],
        _make_service_type(
            cast(type[IdlStruct], request),
            cast(type[IdlStruct], response),
            resolved_event_type,
            service_type_name,
            module_name,
        ),
    )
