import hashlib
from dataclasses import dataclass, field, fields
from collections.abc import Mapping as MappingABC
from typing import (
    Any,
    ClassVar,
    Final,
    Generic,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Self,
    Sequence,
    Type,
    TypeAlias,
    TypeGuard,
    TypeVar,
    cast,
    get_args,
    get_type_hints,
    overload,
)

import cyclonedds_idl as _idl

from . import DISTRO, Distro
from .utils.description import (
    cyclonedds_struct_to_ros_type_description_json,
    ros2_type_hash_from_json,
)
from .utils.idl import (
    IdlMetaIgnoreFinal,
    coerce_byte_sequence,
    coerce_uint8_sequence,
    is_byte_sequence_annotation,
    is_idl_struct_type,
    is_uint8_sequence_annotation,
    to_ros_byte_sequence,
    unwrap_annotated,
)

types = _idl.types


class IdlStruct(_idl.IdlStruct, metaclass=IdlMetaIgnoreFinal):

    def serialize(
        self,
        buffer: Optional[_idl.Buffer] = None,
        endianness: Optional[_idl.Endianness] = None,
        use_version_2: Optional[bool] = None,
    ) -> bytes:
        """
        Serialize this IDL object, using a placeholder for truly empty messages.

        Args:
            buffer: Optional serialization buffer.
            endianness: Optional endianness override.
            use_version_2: Optional XCDR v2 override.

        Returns:
            Serialized bytes.
        """
        if len(getattr(type(self), "__annotations__", {})) == 0:
            # ROS 2 cannot send a truly empty message with only a header
            return DummyEmpty().serialize()
        return super().serialize(buffer, endianness, use_version_2)

    @classmethod
    def json_type_description(
        cls,
        *,
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
        return cyclonedds_struct_to_ros_type_description_json(
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
        return ros2_type_hash_from_json(cls.json_type_description())

    @classmethod
    def hash_rihs01(cls) -> str:
        """
        Compute the RIHS01 hash string for this type.
        """
        return f"RIHS01_{cls._hash_rihs01_raw().hexdigest()}"

    @classmethod
    def get_type_name(cls) -> str:
        """
        Return the ROS type name stored on the class.
        """
        return getattr(cls, "__idl_typename__", "")

    @classmethod
    def get_ros_type(cls) -> type:
        """
        Resolve the matching ROS Python type.
        """
        from importlib import import_module

        module_name, class_name = cls.get_type_name().replace("/", ".").rsplit(".", 1)
        mod = import_module(module_name)
        resolved_name = f"{module_name}.{class_name}"

        try:
            if DISTRO == Distro.HUMBLE:
                if class_name.endswith("_Request"):
                    service_name = class_name.removesuffix("_Request")
                    resolved_name = f"{module_name}.{service_name}.Request"
                    return getattr(mod, service_name).Request
                if class_name.endswith("_Response"):
                    service_name = class_name.removesuffix("_Response")
                    resolved_name = f"{module_name}.{service_name}.Response"
                    return getattr(mod, service_name).Response
                if class_name.endswith("_Event"):
                    service_name = class_name.removesuffix("_Event")
                    resolved_name = f"{module_name}.{service_name}.Event"
                    return getattr(mod, service_name).Event

            return getattr(mod, class_name)
        except AttributeError as exc:
            raise AttributeError(
                f"ROS equivalent for {cls.get_type_name()} does not seem to exist "
                f"in this runtime (DISTRO={DISTRO.value}). Tried {resolved_name}."
            ) from exc

    @classmethod
    def has_ros_type(cls) -> bool:
        """
        Check whether the matching ROS Python type is available in this runtime.
        """
        try:
            cls.get_ros_type()
        except (AttributeError, ImportError, ModuleNotFoundError):
            return False
        return True

    @classmethod
    def to_ros_type(cls) -> type:
        """
        Resolve the matching ROS Python type.
        """
        return cls.get_ros_type()

    def to_ros(self) -> object:
        """
        Convert this IDL object to the matching ROS message.
        """
        ros_msg = type(self).get_ros_type()()
        type_hints = get_type_hints(type(self), include_extras=True)

        for f in fields(self):
            if not hasattr(ros_msg, f.name):
                continue

            src_type = type_hints.get(f.name, f.type)
            src_value = getattr(self, f.name)
            dst_value = getattr(ros_msg, f.name)
            setattr(ros_msg, f.name, self._to_ros_value(src_type, src_value, dst_value))

        return ros_msg

    @classmethod
    def from_ros(cls, msg: object) -> Self:
        """
        Convert a ROS message to this IDL type.

        Args:
            msg: Matching ROS message instance.

        Returns:
            Converted IDL instance.
        """
        if isinstance(msg, cls):
            return msg

        ros_type = cls.get_ros_type()
        if not isinstance(msg, ros_type):
            raise TypeError(
                f"{cls.__name__}.from_ros() expected {ros_type.__module__}.{ros_type.__name__}, "
                f"got {type(msg).__module__}.{type(msg).__name__}"
            )

        type_hints = get_type_hints(cls, include_extras=True)
        kwargs: dict[str, Any] = {}

        for f in fields(cls):
            if not hasattr(msg, f.name):
                raise AttributeError(
                    f"ROS message {type(msg).__module__}.{type(msg).__name__} "
                    f"has no field {f.name!r}"
                )

            dst_type = type_hints.get(f.name, f.type)
            src_value = getattr(msg, f.name)
            kwargs[f.name] = cls._from_ros_value(dst_type, src_value)
        final = cls()
        for k, v in kwargs.items():
            setattr(final, k, v)
        return final

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
        if value is None:
            return None

        if is_uint8_sequence_annotation(dst_type):
            return coerce_uint8_sequence(value)
        if is_byte_sequence_annotation(dst_type):
            return coerce_byte_sequence(value)

        dst_type, _ = unwrap_annotated(dst_type)

        # Nested ROS message -> nested IdlStruct
        if isinstance(dst_type, type) and issubclass(dst_type, IdlStruct):
            return dst_type.from_ros(value)

        # sequence[...] / array[...] / list[...] style annotations
        args = get_args(dst_type) or getattr(dst_type, "__args__", ())
        if (
            args
            and isinstance(value, Sequence)
            and not isinstance(value, (str, bytes, bytearray))
        ):
            elem_type = args[0]
            return [cls._from_ros_value(elem_type, item) for item in value]

        # bytes -> int
        if isinstance(value, bytes):
            return int.from_bytes(value)

        # Primitive / already compatible
        return value

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
        if value is None:
            return None

        if isinstance(value, IdlStruct):
            return value.to_ros()

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
            if isinstance(elem_type, type) and issubclass(elem_type, IdlStruct):
                return [cls._to_ros_value(elem_type, item) for item in value]
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
    if isinstance(value, IdlStruct):
        field_annotations = get_type_hints(type(value), include_extras=True)
        return {
            field.name: message_to_plain_data(
                getattr(value, field.name),
                field_annotations.get(field.name, field.type),
            )
            for field in fields(value)
        }

    if is_uint8_sequence_annotation(annotation):
        return coerce_uint8_sequence(value)
    if is_byte_sequence_annotation(annotation):
        return coerce_byte_sequence(value)

    if hasattr(value, "get_fields_and_field_types"):
        if is_idl_struct_type(annotation, IdlStruct):
            struct_type, _ = unwrap_annotated(annotation)
            field_annotations = get_type_hints(struct_type, include_extras=True)
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
    stamp: Time = field(default_factory=lambda *_: Time())
    client_gid: types.array[types.uint8, 16] = field(
        default_factory=lambda: bytes(16)
    )
    sequence_number: types.int64 = 0


RequestT = TypeVar("RequestT", bound=IdlStruct)
ResponseT = TypeVar("ResponseT", bound=IdlStruct)


class IdlServiceEventStruct(IdlStruct, Generic[RequestT, ResponseT]):
    info: ServiceEventInfo
    request: types.sequence[RequestT, 1]
    response: types.sequence[ResponseT, 1]


EventT = TypeVar("EventT", bound=IdlStruct)


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
        *,
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
    request_typename = request_type.get_type_name()
    response_typename = response_type.get_type_name()

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
    *,
    service_typename: str,
    module_name: str,
    request_type: type[RequestT],
    response_type: type[ResponseT],
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
            "info": ServiceEventInfo,
            "request": types.sequence[request_type, 1],
            "response": types.sequence[response_type, 1],
        },
        "info": field(default_factory=ServiceEventInfo),
        "request": field(default_factory=list),
        "response": field(default_factory=list),
    }
    event_type = cast(
        type[IdlServiceEventStruct[RequestT, ResponseT]],
        dataclass(
            IdlMetaIgnoreFinal(
                event_name,
                (IdlServiceEventStruct,),
                event_namespace,
                typename=event_typename,
            )
        ),
    )
    event_type.__idl_typename__ = event_typename
    return event_type


AnyIdlServiceEvent: TypeAlias = IdlStruct
AnyIdlService: TypeAlias = IdlServiceStruct[IdlStruct, IdlStruct, IdlStruct]
AnyIdlServiceType: TypeAlias = IdlServiceType[IdlStruct, IdlStruct, IdlStruct]


SERVICE_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    {"request_message", "response_message", "event_message"}
)


def is_service_type(obj: Any) -> TypeGuard[type[AnyIdlService]]:
    """
    Check whether an object looks like an IDL service type.
    """
    if not isinstance(obj, type):
        return False
    try:
        if not issubclass(obj, IdlStruct):
            return False
    except TypeError:
        return False

    dataclass_fields = getattr(obj, "__dataclass_fields__", {})
    return SERVICE_FIELD_NAMES.issubset(dataclass_fields)


@overload
def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    *,
    event_type: type[EventT],
    _module_name: str | None = None,
) -> IdlServiceType[RequestT, ResponseT, EventT]: ...


@overload
def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    *,
    _module_name: str | None = None,
) -> IdlServiceType[
    RequestT,
    ResponseT,
    IdlServiceEventStruct[RequestT, ResponseT],
]: ...


def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    *,
    event_type: type[EventT] | None = None,
    _module_name: str | None = None,
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
    if not issubclass(request_type, IdlStruct):
        raise TypeError(
            f"request_type must inherit from IdlStruct, got {request_type!r}"
        )
    if not issubclass(response_type, IdlStruct):
        raise TypeError(
            f"response_type must inherit from IdlStruct, got {response_type!r}"
        )

    service_typename = _service_typename_from_message_types(request_type, response_type)
    service_name = service_typename.rsplit("/", 1)[1]
    module_name = _module_name or request_type.__module__
    uses_generated_event_type = event_type is None
    if event_type is None:
        resolved_event_type: type[IdlStruct] = _make_service_event_type(
            service_typename=service_typename,
            module_name=module_name,
            request_type=request_type,
            response_type=response_type,
        )
    else:
        if not issubclass(event_type, IdlStruct):
            raise TypeError(
                f"event_type must inherit from IdlStruct, got {event_type!r}"
            )
        expected_event_typename = f"{service_typename}_Event"
        if event_type.get_type_name() != expected_event_typename:
            raise ValueError(
                f"event_type must have type name {expected_event_typename!r}, "
                f"got {event_type.get_type_name()!r}"
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
        IdlMetaIgnoreFinal(
            service_name,
            (IdlServiceStruct,),
            service_namespace,
            typename=service_typename,
        )
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
