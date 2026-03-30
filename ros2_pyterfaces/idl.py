import hashlib
from dataclasses import dataclass, field
from collections.abc import Mapping as MappingABC
from typing import (
    Any,
    ClassVar,
    Final,
    Generic,
    Literal,
    Mapping,
    Protocol,
    Self,
    Sequence,
    TypeAlias,
    TypeGuard,
    TypeVar,
    cast,
    get_args,
    overload,
)

from . import DISTRO, Distro
from .idl_types import types
from .utils.description import (
    ros2_type_hash_from_json,
    schema_to_ros_type_description_json,
)
from .utils.idl import (
    coerce_byte_sequence,
    coerce_uint8_sequence,
    get_message_type_name,
    is_byte_sequence_annotation,
    is_idl_struct_type,
    is_message_type,
    is_uint8_sequence_annotation,
    message_field_annotations,
    message_field_names,
    to_ros_byte_sequence,
    unwrap_annotated,
)

SchemaT = TypeVar("SchemaT")


def _schema_type(value_or_type: Any) -> type[Any]:
    return value_or_type if isinstance(value_or_type, type) else type(value_or_type)


def json_type_description(
    value_or_type: type[Any] | Any,
    root_type_name: str | None = None,
    type_name_overrides: Mapping[type, str] | None = None,
    indent: int = 2,
) -> str:
    """
    Build the ROS 2 type description JSON for a schema class.
    """
    return schema_to_ros_type_description_json(
        _schema_type(value_or_type),
        root_type_name=root_type_name,
        type_name_overrides=type_name_overrides,
        indent=indent,
    )


def _hash_rihs01_raw(value_or_type: type[Any] | Any) -> "hashlib._Hash":
    """
    Compute the raw RIHS01 hash object for a schema class.
    """
    return ros2_type_hash_from_json(json_type_description(value_or_type))


def hash_rihs01(value_or_type: type[Any] | Any) -> str:
    """
    Compute the RIHS01 hash string for a schema class.
    """
    return f"RIHS01_{_hash_rihs01_raw(value_or_type).hexdigest()}"


def get_type_name(value_or_type: type[Any] | Any) -> str:
    """
    Return the ROS type name stored on a schema class.
    """
    return get_message_type_name(value_or_type)


_HUMBLE_SERVICE_SUFFIXES: Final[tuple[tuple[str, str], ...]] = (
    ("_Request", "Request"),
    ("_Response", "Response"),
    ("_Event", "Event"),
)


def _get_ros_module_attr(mod: Any, module_name: str, class_name: str) -> type:
    """
    Resolve a class from a ROS module, applying distro-specific name remapping.

    On Humble, service request/response/event classes are nested under the
    service class (e.g. ``SetBool.Request``) instead of being top-level
    (``SetBool_Request``).
    """
    if DISTRO == Distro.HUMBLE:
        for suffix, inner in _HUMBLE_SERVICE_SUFFIXES:
            if class_name.endswith(suffix):
                service_name = class_name.removesuffix(suffix)
                return getattr(getattr(mod, service_name), inner)
    return getattr(mod, class_name)


def get_ros_type(
    value_or_type: type[Any] | Any,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> type:
    """
    Resolve the matching ROS Python type for a schema class.
    """
    schema_type = _schema_type(value_or_type)

    if idl_to_ros_types is not None and schema_type in idl_to_ros_types:
        return idl_to_ros_types[schema_type]

    from importlib import import_module

    type_name = get_type_name(schema_type)
    if "/" not in type_name:
        raise ValueError(
            f"No ROS type mapping available for "
            f"{schema_type.__module__}.{schema_type.__qualname__}. "
            "Pass idl_to_ros_types=... or set __idl_typename__."
        )

    module_name, class_name = type_name.replace("/", ".").rsplit(".", 1)
    mod = import_module(module_name)

    try:
        return _get_ros_module_attr(mod, module_name, class_name)
    except AttributeError as exc:
        raise AttributeError(
            f"ROS equivalent for {get_type_name(schema_type)} does not seem to exist "
            f"in this runtime (DISTRO={DISTRO.value})."
        ) from exc


def has_ros_type(
    value_or_type: type[Any] | Any,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> bool:
    """
    Check whether the matching ROS Python type is available in this runtime.
    """
    try:
        get_ros_type(value_or_type, idl_to_ros_types=idl_to_ros_types)
    except (AttributeError, ImportError, ModuleNotFoundError, ValueError):
        return False
    return True


def to_ros_type(
    value_or_type: type[Any] | Any,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> type:
    """
    Resolve the matching ROS Python type for a schema class.
    """
    return get_ros_type(value_or_type, idl_to_ros_types=idl_to_ros_types)


def _from_ros_value(
    dst_type: Any,
    value: Any,
    ros_to_idl_types: Mapping[type[Any], type[Any]] | None = None,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> Any:
    """
    Convert one ROS field value to its IDL-side value.
    """
    if value is None:
        return None

    if ros_to_idl_types is not None:
        mapped_idl_type = ros_to_idl_types.get(type(value))
        if mapped_idl_type is not None and is_message_type(
            mapped_idl_type, struct_base=IdlStruct
        ):
            return from_ros(
                cast(type[Any], mapped_idl_type),
                value,
                ros_to_idl_types=ros_to_idl_types,
                idl_to_ros_types=idl_to_ros_types,
            )

    if is_uint8_sequence_annotation(dst_type):
        return coerce_uint8_sequence(value)
    if is_byte_sequence_annotation(dst_type):
        return coerce_byte_sequence(value)

    dst_type, _ = unwrap_annotated(dst_type)

    if is_message_type(dst_type, struct_base=IdlStruct):
        return from_ros(
            cast(type[Any], dst_type),
            value,
            idl_to_ros_types=idl_to_ros_types,
        )

    args = get_args(dst_type) or getattr(dst_type, "__args__", ())
    if (
        args
        and isinstance(value, Sequence)
        and not isinstance(value, (str, bytes, bytearray))
    ):
        elem_type = args[0]
        return [
            _from_ros_value(
                elem_type,
                item,
                idl_to_ros_types=idl_to_ros_types,
            )
            for item in value
        ]

    if isinstance(value, bytes):
        return int.from_bytes(value)

    return value


def from_ros(
    schema_type: type[SchemaT],
    msg: object,
    ros_to_idl_types: Mapping[type[Any], type[Any]] | None = None,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> SchemaT:
    """
    Convert a ROS message to a schema instance.
    """
    if isinstance(msg, schema_type):
        return msg

    ros_type = get_ros_type(schema_type, idl_to_ros_types=idl_to_ros_types)
    if not isinstance(msg, ros_type):
        raise TypeError(
            f"{schema_type.__name__}.from_ros() expected "
            f"{ros_type.__module__}.{ros_type.__name__}, "
            f"got {type(msg).__module__}.{type(msg).__name__}"
        )

    type_hints = message_field_annotations(schema_type, include_extras=True)
    kwargs: dict[str, Any] = {}

    for field_name in message_field_names(schema_type):
        if not hasattr(msg, field_name):
            raise AttributeError(
                f"ROS message {type(msg).__module__}.{type(msg).__name__} "
                f"has no field {field_name!r}"
            )

        dst_type = type_hints[field_name]
        src_value = getattr(msg, field_name)
        kwargs[field_name] = _from_ros_value(
            dst_type,
            src_value,
            ros_to_idl_types=ros_to_idl_types,
            idl_to_ros_types=idl_to_ros_types,
        )

    try:
        return schema_type(**kwargs)
    except TypeError as exc:
        raise TypeError(
            f"{schema_type.__module__}.{schema_type.__qualname__} could not be "
            "constructed with from_ros() kwargs. Ensure the constructor accepts "
            "all field names as keyword arguments."
        ) from exc


def _to_ros_value(
    src_type: Any,
    value: Any,
    dst_value: Any = None,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> Any:
    """
    Convert one schema field value to its ROS-side value.
    """
    if value is None:
        return None

    if is_message_type(type(value), struct_base=IdlStruct):
        return to_ros(value, idl_to_ros_types=idl_to_ros_types)

    if is_byte_sequence_annotation(src_type):
        return to_ros_byte_sequence(value)

    src_type, _ = unwrap_annotated(src_type)
    args = get_args(src_type) or getattr(src_type, "__args__", ())
    if (
        args
        and isinstance(value, Sequence)
        and not isinstance(value, (str, bytes, bytearray))
    ):
        elem_type = args[0]
        if is_message_type(elem_type, struct_base=IdlStruct):
            return [
                _to_ros_value(
                    elem_type,
                    item,
                    idl_to_ros_types=idl_to_ros_types,
                )
                for item in value
            ]
        return value

    if isinstance(value, (bytes, bytearray, memoryview)):
        if isinstance(dst_value, bytes):
            return bytes(value)
        return list(value)

    if isinstance(dst_value, bytes):
        return bytes([int(value)])

    if src_type in (float, types.float32, types.float64):
        return float(value)

    if src_type in (
        int,
        types.byte,
        types.char,
        types.int8,
        types.uint8,
        types.int16,
        types.uint16,
        types.int32,
        types.uint32,
        types.int64,
        types.uint64,
    ):
        return int(value)

    return value


def to_ros(
    value: Any,
    idl_to_ros_types: Mapping[type[Any], type[Any]] | None = None,
) -> object:
    """
    Convert a schema instance to the matching ROS message.
    """
    schema_type = type(value)
    ros_msg = get_ros_type(schema_type, idl_to_ros_types=idl_to_ros_types)()
    type_hints = message_field_annotations(schema_type, include_extras=True)

    for field_name in message_field_names(schema_type):
        if not hasattr(ros_msg, field_name):
            continue

        src_type = type_hints[field_name]
        src_value = getattr(value, field_name)
        dst_value = getattr(ros_msg, field_name)
        setattr(
            ros_msg,
            field_name,
            _to_ros_value(
                src_type,
                src_value,
                dst_value,
                idl_to_ros_types=idl_to_ros_types,
            ),
        )

    return ros_msg


class IdlStruct:
    __slots__ = ()
    __idl_typename__: ClassVar = ""

    @classmethod
    def json_type_description(
        cls,
        root_type_name: str | None = None,
        type_name_overrides: Mapping[type, str] | None = None,
        indent: int = 2,
    ) -> str:
        """
        Build the ROS 2 type description JSON for this class.

        Args:
            root_type_name: Optional root ROS type name.
            type_name_overrides: Optional nested type name overrides.
            indent: JSON indentation level.

        Returns:
            Type description JSON.
        """
        return json_type_description(
            cls,
            root_type_name=root_type_name,
            type_name_overrides=type_name_overrides,
            indent=indent,
        )

    @classmethod
    def _hash_rihs01_raw(cls) -> "hashlib._Hash":
        """
        Compute the raw RIHS01 hash object for this type.
        """
        return _hash_rihs01_raw(cls)

    @classmethod
    def hash_rihs01(cls) -> str:
        """
        Compute the RIHS01 hash string for this type.
        """
        return hash_rihs01(cls)

    @classmethod
    def get_type_name(cls) -> str:
        """
        Return the ROS type name stored on the class.
        """
        return get_type_name(cls)

    @classmethod
    def get_ros_type(cls) -> type:
        """
        Resolve the matching ROS Python type.
        """
        return get_ros_type(cls)

    @classmethod
    def has_ros_type(cls) -> bool:
        """
        Check whether the matching ROS Python type is available in this runtime.
        """
        return has_ros_type(cls)

    @classmethod
    def to_ros_type(cls) -> type:
        """
        Resolve the matching ROS Python type.
        """
        return to_ros_type(cls)

    def to_ros(self) -> object:
        """
        Convert this IDL object to the matching ROS message.
        """
        return to_ros(self)

    @classmethod
    def from_ros(cls, msg: object) -> Self:
        """
        Convert a ROS message to this IDL type.

        Args:
            msg: Matching ROS message instance.

        Returns:
            Converted IDL instance.
        """
        return from_ros(cls, msg)

    @classmethod
    def _from_ros_value(cls, dst_type: Any, value: Any) -> Any:
        """
        Convert one ROS field value to its IDL-side value.

        Args:
            dst_type: Target field type.
            value: ROS field value.

        Returns:
            Converted Python value.
        """
        return _from_ros_value(dst_type, value)

    @classmethod
    def _to_ros_value(cls, src_type: Any, value: Any, dst_value: Any = None) -> Any:
        """
        Convert one IDL field value to its ROS-side value.

        Args:
            src_type: Source field type.
            value: IDL field value.
            dst_value: Current ROS destination value.

        Returns:
            Value for the ROS field.
        """
        return _to_ros_value(src_type, value, dst_value)


def message_to_plain_data(value: Any, annotation: Any | None = None) -> Any:
    """
    Convert an IDL struct or ROS message object into normalized plain data.

    This is intended for value comparisons, tests, snapshots, and other cases
    where a message should be represented as nested Python data structures
    instead of ROS/IDL runtime objects. Structs and ROS messages become dicts,
    generic sequences become lists, annotated ``uint8`` sequences keep the
    library's canonical ``bytes`` representation, and annotated ``byte``
    sequences normalize to ``list[int]`` when their annotation is available.

    Args:
        value: IDL struct, ROS message, or nested message field value.
        annotation: Optional field or struct annotation used to preserve richer
            normalization, especially for ROS-side ``uint8`` sequences.

    Returns:
        A normalized tree made of dicts, lists, scalars, and bytes.
    """
    if is_message_type(type(value), struct_base=IdlStruct):
        field_annotations = message_field_annotations(type(value), include_extras=True)
        return {
            field_name: message_to_plain_data(
                getattr(value, field_name),
                field_annotations.get(field_name),
            )
            for field_name in message_field_names(type(value))
        }

    if is_uint8_sequence_annotation(annotation):
        return coerce_uint8_sequence(value)
    if is_byte_sequence_annotation(annotation):
        return coerce_byte_sequence(value)

    if hasattr(value, "get_fields_and_field_types"):
        if is_idl_struct_type(annotation, IdlStruct):
            struct_type, _ = unwrap_annotated(annotation)
            field_annotations = message_field_annotations(
                struct_type, include_extras=True
            )
            return {
                field_name: message_to_plain_data(
                    getattr(value, field_name),
                    field_annotations.get(field_name),
                )
                for field_name in value.get_fields_and_field_types().keys()
            }

        return {
            field_name: message_to_plain_data(getattr(value, field_name))
            for field_name in value.get_fields_and_field_types().keys()
        }

    if isinstance(value, MappingABC):
        return {key: message_to_plain_data(item) for key, item in value.items()}

    if hasattr(value, "tolist") and not isinstance(value, (str, bytes, bytearray)):
        return message_to_plain_data(value.tolist(), annotation)

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [message_to_plain_data(item) for item in value]

    return value


@dataclass
class Time(IdlStruct):
    __idl_typename__: ClassVar[str] = "builtin_interfaces/msg/Time"
    sec: types.int32 = 0
    nanosec: types.uint32 = 0


@dataclass
class ServiceEventInfo(IdlStruct):
    __idl_typename__: ClassVar[str] = "service_msgs/msg/ServiceEventInfo"
    REQUEST_SENT: ClassVar[Literal[0]] = 0
    REQUEST_RECEIVED: ClassVar[Literal[1]] = 1
    RESPONSE_SENT: ClassVar[Literal[2]] = 2
    RESPONSE_RECEIVED: ClassVar[Literal[3]] = 3

    event_type: types.uint8 = 0
    stamp: Time = field(default_factory=lambda *_: Time())
    client_gid: types.array[types.uint8, 16] = field(
        default_factory=lambda: bytes(16)
    )
    sequence_number: types.int64 = 0


RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class IdlServiceEventStruct(IdlStruct, Generic[RequestT, ResponseT]):
    info: ServiceEventInfo
    request: types.sequence[RequestT, 1]
    response: types.sequence[ResponseT, 1]


EventT = TypeVar("EventT")


class IdlServiceStruct(IdlStruct, Generic[RequestT, ResponseT, EventT]):
    request_message: RequestT
    response_message: ResponseT
    event_message: EventT


class IdlServiceType(Protocol[RequestT, ResponseT, EventT]):
    Request: type[RequestT]
    Response: type[ResponseT]
    Event: type[EventT]

    def __call__(
        self,
        request_message: RequestT = ...,
        response_message: ResponseT = ...,
        event_message: EventT = ...,
    ) -> IdlServiceStruct[RequestT, ResponseT, EventT]: ...

    def get_type_name(self) -> str: ...
    def get_ros_type(self) -> type: ...
    def to_ros_type(self) -> type: ...
    def json_type_description(
        self,
        root_type_name: str | None = ...,
        type_name_overrides: Mapping[type, str] | None = ...,
        indent: int = ...,
    ) -> str: ...
    def hash_rihs01(self) -> str: ...


def _service_typename_from_message_types(
    request_type: type[RequestT], response_type: type[ResponseT]
) -> str:
    """
    Derive the shared service type name from request and response types.

    Args:
        request_type: Request message type.
        response_type: Response message type.

    Returns:
        Shared service type name.
    """
    request_typename = get_type_name(request_type)
    response_typename = get_type_name(response_type)

    if not request_typename.endswith("_Request"):
        raise ValueError(
            f"{request_type.__name__} must have a type name ending with '_Request', "
            f"got {request_typename!r}"
        )
    if not response_typename.endswith("_Response"):
        raise ValueError(
            f"{response_type.__name__} must have a type name ending with '_Response', "
            f"got {response_typename!r}"
        )

    service_typename = request_typename.removesuffix("_Request")
    expected_response_typename = f"{service_typename}_Response"
    if response_typename != expected_response_typename:
        raise ValueError(
            "Request and response types must share the same service type name, "
            f"got {request_typename!r} and {response_typename!r}"
        )
    return service_typename


def _make_service_event_type(
    service_typename: str,
    module_name: str,
    request_type: type[RequestT],
    response_type: type[ResponseT],
    type_namespace: Any = types,
    service_event_info_type: type[Any] = ServiceEventInfo,
    service_event_base: type[Any] = IdlServiceEventStruct,
    metaclass: type[type[Any]] = type,
) -> type[IdlServiceEventStruct[RequestT, ResponseT]]:
    """
    Create the generated ``_Event`` type for a service.

    Args:
        service_typename: ROS service type name.
        module_name: Python module name.
        request_type: Request message type.
        response_type: Response message type.

    Returns:
        Generated event type.
    """
    service_name = service_typename.rsplit("/", 1)[1]
    event_name = f"{service_name}_Event"
    event_typename = f"{service_typename}_Event"
    event_namespace = {
        "__module__": module_name,
        "__idl_typename__": event_typename,
        "__annotations__": {
            "info": service_event_info_type,
            "request": type_namespace.sequence[request_type, 1],
            "response": type_namespace.sequence[response_type, 1],
        },
        "info": field(default_factory=service_event_info_type),
        "request": field(default_factory=list),
        "response": field(default_factory=list),
    }
    event_type = cast(
        type[IdlServiceEventStruct[RequestT, ResponseT]],
        dataclass(metaclass(event_name, (service_event_base,), event_namespace)),
    )
    event_type.__idl_typename__ = event_typename
    return event_type


AnyIdlServiceEvent: TypeAlias = Any
AnyIdlService: TypeAlias = IdlServiceStruct[Any, Any, Any]
AnyIdlServiceType: TypeAlias = IdlServiceType[Any, Any, Any]


SERVICE_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    {"request_message", "response_message", "event_message"}
)


def is_service_type(obj: Any) -> TypeGuard[type[AnyIdlService]]:
    """
    Check whether an object looks like an IDL service type.
    """
    return isinstance(obj, type) and SERVICE_FIELD_NAMES.issubset(
        set(message_field_names(obj))
    )


@overload
def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    event_type: type[EventT],
    _module_name: str | None = None,
) -> IdlServiceType[RequestT, ResponseT, EventT]: ...


@overload
def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    _module_name: str | None = None,
) -> IdlServiceType[
    RequestT,
    ResponseT,
    IdlServiceEventStruct[RequestT, ResponseT],
]: ...


def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    event_type: type[EventT] | None = None,
    _module_name: str | None = None,
    _struct_base: type[Any] = IdlStruct,
    _type_namespace: Any = types,
    _metaclass: type[type[Any]] = type,
    _service_event_info_type: type[Any] = ServiceEventInfo,
    _service_event_base: type[Any] = IdlServiceEventStruct,
    _service_base: type[Any] = IdlServiceStruct,
) -> (
    IdlServiceType[
        RequestT,
        ResponseT,
        EventT,
    ]
    | IdlServiceType[
        RequestT,
        ResponseT,
        IdlServiceEventStruct[RequestT, ResponseT],
    ]
):
    """
    Generate an IDL service type from request and response message types.

    Args:
        request_type: Request message type.
        response_type: Response message type.
        event_type: Optional explicit event message type.
        _module_name: Optional Python module name.

    Returns:
        Generated service type.
    """
    if not is_message_type(request_type, struct_base=_struct_base):
        raise TypeError(
            "request_type must be an annotated schema class, "
            f"got {request_type!r}"
        )
    if not is_message_type(response_type, struct_base=_struct_base):
        raise TypeError(
            "response_type must be an annotated schema class, "
            f"got {response_type!r}"
        )

    service_typename = _service_typename_from_message_types(request_type, response_type)
    service_name = service_typename.rsplit("/", 1)[1]
    module_name = _module_name or request_type.__module__
    uses_generated_event_type = event_type is None
    if event_type is None:
        resolved_event_type: type[Any] = _make_service_event_type(
            service_typename=service_typename,
            module_name=module_name,
            request_type=request_type,
            response_type=response_type,
            type_namespace=_type_namespace,
            service_event_info_type=_service_event_info_type,
            service_event_base=_service_event_base,
            metaclass=_metaclass,
        )
    else:
        if not is_message_type(event_type, struct_base=_struct_base):
            raise TypeError(
                "event_type must be an annotated schema class, "
                f"got {event_type!r}"
            )
        expected_event_typename = f"{service_typename}_Event"
        if get_type_name(event_type) != expected_event_typename:
            raise ValueError(
                f"event_type must have type name {expected_event_typename!r}, "
                f"got {get_type_name(event_type)!r}"
            )
        resolved_event_type = event_type

    service_namespace = {
        "__module__": module_name,
        "__idl_typename__": service_typename,
        "__annotations__": {
            "request_message": request_type,
            "response_message": response_type,
            "event_message": resolved_event_type,
        },
        "Request": request_type,
        "Response": response_type,
        "Event": resolved_event_type,
        "request_message": field(default_factory=request_type),
        "response_message": field(default_factory=response_type),
        "event_message": field(default_factory=resolved_event_type),
    }
    service_type = dataclass(
        _metaclass(service_name, (_service_base,), service_namespace)
    )
    service_type.__idl_typename__ = service_typename
    if uses_generated_event_type:
        return cast(
            IdlServiceType[
                RequestT,
                ResponseT,
                IdlServiceEventStruct[RequestT, ResponseT],
            ],
            service_type,
        )
    return cast(
        IdlServiceType[
            RequestT,
            ResponseT,
            EventT,
        ],
        service_type,
    )
