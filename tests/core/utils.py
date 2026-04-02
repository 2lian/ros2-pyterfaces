from __future__ import annotations

from collections.abc import Mapping
from typing import Any, List

from ros2_pyterfaces.core import CoreSchema, all_msgs, all_srvs, random_message


def _is_core_schema(value: Any) -> bool:
    return isinstance(value, Mapping) and isinstance(value.get("__typename"), str)


def _collect_unique_schemas(namespace: Mapping[str, Any]) -> list[CoreSchema]:
    by_typename: dict[str, CoreSchema] = {}
    for value in namespace.values():
        if not _is_core_schema(value):
            continue
        schema = dict(value)
        by_typename.setdefault(schema["__typename"], schema)
    return [by_typename[type_name] for type_name in sorted(by_typename)]


def _is_message_schema(schema: CoreSchema) -> bool:
    return "/msg/" in schema["__typename"]


def _is_service_schema(schema: CoreSchema) -> bool:
    type_name = schema["__typename"]
    return "/srv/" in type_name and not (
        type_name.endswith("_Request")
        or type_name.endswith("_Response")
        or type_name.endswith("_Event")
    )


def _is_service_message_schema(schema: CoreSchema) -> bool:
    type_name = schema["__typename"]
    return "/srv/" in type_name and (
        type_name.endswith("_Request")
        or type_name.endswith("_Response")
        or type_name.endswith("_Event")
    )


ALL_MESSAGE_SCHEMAS = _collect_unique_schemas(vars(all_msgs))
ALL_SERVICE_SCHEMAS = _collect_unique_schemas(vars(all_srvs))

MESSAGE_SCHEMAS: list[CoreSchema] = [
    schema for schema in ALL_MESSAGE_SCHEMAS if _is_message_schema(schema)
]
MESSAGE_SCHEMA_IDS: List[str] = [schema["__typename"] for schema in MESSAGE_SCHEMAS]
MESSAGE_VALUES: list[dict[str, Any]] = [
    random_message(schema) for schema in MESSAGE_SCHEMAS
]
MESSAGE_VALUE_IDS: List[str] = [message["__typename"] for message in MESSAGE_VALUES]

SERVICE_SCHEMAS: list[CoreSchema] = [
    schema for schema in ALL_SERVICE_SCHEMAS if _is_service_schema(schema)
]
SERVICE_SCHEMA_IDS: List[str] = [schema["__typename"] for schema in SERVICE_SCHEMAS]
SERVICE_VALUES: list[dict[str, Any]] = [
    random_message(schema) for schema in SERVICE_SCHEMAS
]
SERVICE_VALUE_IDS: List[str] = [message["__typename"] for message in SERVICE_VALUES]

SERVICE_MESSAGE_SCHEMAS: list[CoreSchema] = [
    schema for schema in ALL_SERVICE_SCHEMAS if _is_service_message_schema(schema)
]
SERVICE_MESSAGE_SCHEMA_IDS: List[str] = [
    schema["__typename"] for schema in SERVICE_MESSAGE_SCHEMAS
]
SERVICE_MESSAGE_VALUES: list[dict[str, Any]] = [
    random_message(schema) for schema in SERVICE_MESSAGE_SCHEMAS
]
SERVICE_MESSAGE_VALUE_IDS: List[str] = [
    message["__typename"] for message in SERVICE_MESSAGE_VALUES
]
