import hashlib
from dataclasses import dataclass, field, fields
from typing import (
    Any,
    ClassVar,
    Final,
    Generic,
    Literal,
    Mapping,
    Optional,
    Self,
    Sequence,
    Type,
    TypeAlias,
    TypeGuard,
    TypeVar,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

import cyclonedds_idl as _idl

from .utils.description import (
    cyclonedds_struct_to_ros_type_description_json,
    ros2_type_hash_from_json,
)

types = _idl.types


# derive from the same metaclass Cyclone already uses
class IdlMetaIgnoreFinal(type(_idl.IdlStruct)):
    def __new__(mcls, name, bases, namespace, **kwargs):
        """
        Create a class while stripping ``Final`` and ``Literal`` field annotations.
        """
        ann = namespace.get("__annotations__")
        if ann:
            # remove only from annotations; keep the class attributes themselves
            for key in list(ann):
                if get_origin(ann[key]) is ClassVar:
                    ann.pop(key)
                elif get_origin(ann[key]) is Literal:
                    ann.pop(key)
                elif get_origin(ann[key]) is Final:
                    ann.pop(key)
        return super().__new__(mcls, name, bases, namespace, **kwargs)


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
        return getattr(mod, class_name)

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
        type_hints = get_type_hints(type(self))

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

        type_hints = get_type_hints(cls)
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


@dataclass
class DummyEmpty(IdlStruct, typename="does/not/matter/empty"):
    structure_needs_at_least_one_member: types.uint8 = 0


from .service_msgs.msg import ServiceEventInfo

RequestT = TypeVar("RequestT", bound=IdlStruct)
ResponseT = TypeVar("ResponseT", bound=IdlStruct)


class IdlServiceEventStruct(IdlStruct, Generic[RequestT, ResponseT]):
    info: ServiceEventInfo
    request: types.sequence[RequestT, 1]
    response: types.sequence[ResponseT, 1]

EventT = TypeVar("EventT", bound=IdlServiceEventStruct)

class IdlServiceStruct(IdlStruct, Generic[RequestT, ResponseT, EventT]):
    request_message: RequestT
    response_message: ResponseT
    event_message: EventT


AnyIdlServiceEvent: TypeAlias = IdlServiceEventStruct[IdlStruct, IdlStruct]
AnyIdlService: TypeAlias = IdlServiceStruct[IdlStruct, IdlStruct, AnyIdlServiceEvent]


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


def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
    *,
    _module_name: str | None = None,
) -> type[
    IdlServiceStruct[
        RequestT, ResponseT, IdlServiceEventStruct[RequestT, ResponseT]
    ]
]:
    """
    Generate an IDL service type from request and response message types.

    Args:
        request_type: Request message type.
        response_type: Response message type.
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
    event_type = _make_service_event_type(
        service_typename=service_typename,
        module_name=module_name,
        request_type=request_type,
        response_type=response_type,
    )
    service_namespace = {
        "__module__": module_name,
        "__idl_typename__": service_typename,
        "__annotations__": {
            "Request": ClassVar[Type[request_type]],
            "Response": ClassVar[Type[response_type]],
            "request_message": request_type,
            "response_message": response_type,
            "event_message": event_type,
        },
        "Request": request_type,
        "Response": response_type,
        "request_message": field(default_factory=request_type),
        "response_message": field(default_factory=response_type),
        "event_message": field(default_factory=event_type),
    }
    service_type = cast(
        type[
            IdlServiceStruct[
                RequestT, ResponseT, IdlServiceEventStruct[RequestT, ResponseT]
            ]
        ],
        dataclass(
            IdlMetaIgnoreFinal(
                service_name,
                (IdlServiceStruct,),
                service_namespace,
                typename=service_typename,
            )
        ),
    )
    service_type.__idl_typename__ = service_typename
    return service_type
