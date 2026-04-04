from .. import Array, BoundedString, CoreSchema, Sequence

FieldType: CoreSchema = {
    "__typename": "type_description_interfaces/msg/FieldType",
    "type_id": "uint8",
    "capacity": "uint64",
    "string_capacity": "uint64",
    "nested_type_name": BoundedString(255),
}

KeyValue: CoreSchema = {
    "__typename": "type_description_interfaces/msg/KeyValue",
    "key": "string",
    "value": "string",
}

TypeSource: CoreSchema = {
    "__typename": "type_description_interfaces/msg/TypeSource",
    "type_name": "string",
    "encoding": "string",
    "raw_file_contents": "string",
}

Field: CoreSchema = {
    "__typename": "type_description_interfaces/msg/Field",
    "name": "string",
    "type": FieldType,
    "default_value": "string",
}

IndividualTypeDescription: CoreSchema = {
    "__typename": "type_description_interfaces/msg/IndividualTypeDescription",
    "type_name": BoundedString(255),
    "fields": Sequence(Field),
}

TypeDescription: CoreSchema = {
    "__typename": "type_description_interfaces/msg/TypeDescription",
    "type_description": IndividualTypeDescription,
    "referenced_type_descriptions": Sequence(IndividualTypeDescription),
}

__all__ = [
    "FieldType",
    "KeyValue",
    "TypeSource",
    "Field",
    "IndividualTypeDescription",
    "TypeDescription",
]
