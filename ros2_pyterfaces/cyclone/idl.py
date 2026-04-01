from dataclasses import dataclass, field
from typing import Any, ClassVar, Generic, Literal, TypeVar, cast

import cyclonedds_idl as _idl

from .. import idl as core_idl
from ..utils.idl import message_field_names, strip_ignored_field_annotations

types = _idl.types

json_type_description = core_idl.json_type_description
hash_rihs01 = core_idl.hash_rihs01
get_type_name = core_idl.get_type_name
get_ros_type = core_idl.get_ros_type
has_ros_type = core_idl.has_ros_type
to_ros_type = core_idl.to_ros_type
to_ros = core_idl.to_ros
from_ros = core_idl.from_ros
message_to_plain_data = core_idl.message_to_plain_data
is_service_type = core_idl.is_service_type
AnyIdlService = core_idl.AnyIdlService
AnyIdlServiceType = core_idl.AnyIdlServiceType


class IdlMetaIgnoreFinal(type(_idl.IdlStruct)):
    def __new__(mcls, name, bases, namespace, **kwargs):
        typename = kwargs.pop("typename", None)
        if typename is not None:
            namespace["__idl_typename__"] = typename
        strip_ignored_field_annotations(namespace)
        return super().__new__(mcls, name, bases, namespace, **kwargs)


class IdlStruct(core_idl.IdlStruct, _idl.IdlStruct, metaclass=IdlMetaIgnoreFinal):
    def __init_subclass__(cls, typename: str | None = None, **kwargs: Any) -> None:
        """ Adds to the class typename="test"):"""
        super().__init_subclass__(**kwargs)
        if typename is not None:
            cls.__idl_typename__ = typename

    def serialize(
        self,
        buffer: _idl.Buffer | None = None,
        endianness: _idl.Endianness | None = None,
        use_version_2: bool | None = None,
    ) -> bytes:
        # if len(message_field_names(type(self))) == 0:
        #     return DummyEmpty().serialize(buffer, endianness, use_version_2)
        return super().serialize(buffer, endianness, use_version_2)


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
    client_gid: types.array[types.uint8, 16] = field(default_factory=lambda: bytes(16))
    sequence_number: types.int64 = 0


RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")
EventT = TypeVar("EventT")


class IdlServiceEventStruct(IdlStruct, Generic[RequestT, ResponseT]):
    info: ServiceEventInfo
    request: types.sequence[RequestT, 1]
    response: types.sequence[ResponseT, 1]


class IdlServiceStruct(IdlStruct, Generic[RequestT, ResponseT, EventT]):
    request_message: RequestT
    response_message: ResponseT
    event_message: EventT


IdlServiceType = core_idl.IdlServiceType


def make_idl_service(
    request_type: type[RequestT],
    response_type: type[ResponseT],
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
    return cast(
        IdlServiceType[
            RequestT,
            ResponseT,
            EventT,
        ]
        | IdlServiceType[
            RequestT,
            ResponseT,
            IdlServiceEventStruct[RequestT, ResponseT],
        ],
        core_idl.make_idl_service(
            request_type,
            response_type,
            event_type=event_type,
            _module_name=_module_name,
            _struct_base=IdlStruct,
            _type_namespace=types,
            _metaclass=IdlMetaIgnoreFinal,
            _service_event_info_type=ServiceEventInfo,
            _service_event_base=IdlServiceEventStruct,
            _service_base=IdlServiceStruct,
        ),
    )


__all__ = [
    "AnyIdlService",
    "AnyIdlServiceType",
    "DummyEmpty",
    "IdlMetaIgnoreFinal",
    "IdlServiceEventStruct",
    "IdlServiceStruct",
    "IdlServiceType",
    "IdlStruct",
    "ServiceEventInfo",
    "Time",
    "from_ros",
    "get_ros_type",
    "get_type_name",
    "has_ros_type",
    "hash_rihs01",
    "is_service_type",
    "json_type_description",
    "make_idl_service",
    "message_to_plain_data",
    "to_ros",
    "to_ros_type",
    "types",
]
