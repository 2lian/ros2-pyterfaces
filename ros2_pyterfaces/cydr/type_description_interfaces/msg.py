from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct

class FieldType(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/msg/FieldType'
    __unsupported_reason__ = (
        'nested_type_name requires bounded string, which cydr does not support'
    )
    pass

class Field(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/msg/Field'
    __unsupported_reason__ = (
        'type references unsupported message FieldType '
        '(bounded string not supported by cydr)'
    )
    pass

class IndividualTypeDescription(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/msg/IndividualTypeDescription'
    __unsupported_reason__ = 'fields is a collection of messages, which cydr does not support'
    pass

class KeyValue(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/msg/KeyValue'
    key: types.string = b''
    value: types.string = b''

class TypeDescription(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/msg/TypeDescription'
    __unsupported_reason__ = 'referenced_type_descriptions is a collection of messages, which cydr does not support'
    pass

class TypeSource(IdlStruct):
    __idl_typename__ = 'type_description_interfaces/msg/TypeSource'
    type_name: types.string = b''
    encoding: types.string = b''
    raw_file_contents: types.string = b''
