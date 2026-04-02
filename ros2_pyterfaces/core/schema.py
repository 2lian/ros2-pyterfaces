from typing import Any

from .types import (
    _EVENT_FIELD,
    _REQUEST_FIELD,
    _RESPONSE_FIELD,
    _TYPENAME_KEY,
    Array,
    CoreSchema,
)


def get_type_name(schema: CoreSchema) -> str:
    type_name = schema.get(_TYPENAME_KEY)
    if not isinstance(type_name, str) or not type_name:
        raise ValueError(
            f"Core schema must contain a non-empty {_TYPENAME_KEY!r} string"
        )
    return type_name


def _service_name_from_request_response(
    request_type_name: str, response_type_name: str
) -> str:
    if not request_type_name.endswith("_Request"):
        raise ValueError(
            f"Request schema type must end with '_Request', got {request_type_name!r}"
        )
    if not response_type_name.endswith("_Response"):
        raise ValueError(
            f"Response schema type must end with '_Response', got {response_type_name!r}"
        )

    from_request = request_type_name.removesuffix("_Request")
    from_response = response_type_name.removesuffix("_Response")
    if from_request != from_response:
        raise ValueError(
            "Request and response type names must share the same service type name, "
            f"got {request_type_name!r} and {response_type_name!r}"
        )
    return from_request


def _default_service_event_info_schema() -> CoreSchema:
    time_schema: CoreSchema = {
        _TYPENAME_KEY: "builtin_interfaces/msg/Time",
        "sec": "int32",
        "nanosec": "uint32",
    }
    return {
        _TYPENAME_KEY: "service_msgs/msg/ServiceEventInfo",
        "event_type": "uint8",
        "stamp": time_schema,
        "client_gid": Array("uint8", 16),
        "sequence_number": "int64",
    }


def make_srv_schema(
    request: CoreSchema,
    response: CoreSchema,
    typename: str | None = None,
) -> CoreSchema:
    request_type_name = get_type_name(request)
    response_type_name = get_type_name(response)

    if typename is None:
        service_type_name = _service_name_from_request_response(
            request_type_name, response_type_name
        )
    else:
        service_type_name = typename

    event_schema: CoreSchema = {
        _TYPENAME_KEY: f"{service_type_name}_Event",
        "info": _default_service_event_info_schema(),
        "request": request,
        "response": response,
    }

    return {
        _TYPENAME_KEY: service_type_name,
        _REQUEST_FIELD: request,
        _RESPONSE_FIELD: response,
        _EVENT_FIELD: event_schema,
    }
