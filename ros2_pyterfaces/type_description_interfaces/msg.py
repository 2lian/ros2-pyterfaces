from dataclasses import dataclass, field
from typing import ClassVar, Literal

from ..idl import IdlStruct, types


@dataclass
class FieldType(IdlStruct, typename="type_description_interfaces/msg/FieldType"):
    FIELD_TYPE_NOT_SET: ClassVar[Literal[0]] = 0
    FIELD_TYPE_NESTED_TYPE: ClassVar[Literal[1]] = 1
    FIELD_TYPE_INT8: ClassVar[Literal[2]] = 2
    FIELD_TYPE_UINT8: ClassVar[Literal[3]] = 3
    FIELD_TYPE_INT16: ClassVar[Literal[4]] = 4
    FIELD_TYPE_UINT16: ClassVar[Literal[5]] = 5
    FIELD_TYPE_INT32: ClassVar[Literal[6]] = 6
    FIELD_TYPE_UINT32: ClassVar[Literal[7]] = 7
    FIELD_TYPE_INT64: ClassVar[Literal[8]] = 8
    FIELD_TYPE_UINT64: ClassVar[Literal[9]] = 9
    FIELD_TYPE_FLOAT: ClassVar[Literal[10]] = 10
    FIELD_TYPE_DOUBLE: ClassVar[Literal[11]] = 11
    FIELD_TYPE_LONG_DOUBLE: ClassVar[Literal[12]] = 12
    FIELD_TYPE_CHAR: ClassVar[Literal[13]] = 13
    FIELD_TYPE_WCHAR: ClassVar[Literal[14]] = 14
    FIELD_TYPE_BOOLEAN: ClassVar[Literal[15]] = 15
    FIELD_TYPE_BYTE: ClassVar[Literal[16]] = 16
    FIELD_TYPE_STRING: ClassVar[Literal[17]] = 17
    FIELD_TYPE_WSTRING: ClassVar[Literal[18]] = 18
    FIELD_TYPE_FIXED_STRING: ClassVar[Literal[19]] = 19
    FIELD_TYPE_FIXED_WSTRING: ClassVar[Literal[20]] = 20
    FIELD_TYPE_BOUNDED_STRING: ClassVar[Literal[21]] = 21
    FIELD_TYPE_BOUNDED_WSTRING: ClassVar[Literal[22]] = 22
    FIELD_TYPE_NESTED_TYPE_ARRAY: ClassVar[Literal[49]] = 49
    FIELD_TYPE_INT8_ARRAY: ClassVar[Literal[50]] = 50
    FIELD_TYPE_UINT8_ARRAY: ClassVar[Literal[51]] = 51
    FIELD_TYPE_INT16_ARRAY: ClassVar[Literal[52]] = 52
    FIELD_TYPE_UINT16_ARRAY: ClassVar[Literal[53]] = 53
    FIELD_TYPE_INT32_ARRAY: ClassVar[Literal[54]] = 54
    FIELD_TYPE_UINT32_ARRAY: ClassVar[Literal[55]] = 55
    FIELD_TYPE_INT64_ARRAY: ClassVar[Literal[56]] = 56
    FIELD_TYPE_UINT64_ARRAY: ClassVar[Literal[57]] = 57
    FIELD_TYPE_FLOAT_ARRAY: ClassVar[Literal[58]] = 58
    FIELD_TYPE_DOUBLE_ARRAY: ClassVar[Literal[59]] = 59
    FIELD_TYPE_LONG_DOUBLE_ARRAY: ClassVar[Literal[60]] = 60
    FIELD_TYPE_CHAR_ARRAY: ClassVar[Literal[61]] = 61
    FIELD_TYPE_WCHAR_ARRAY: ClassVar[Literal[62]] = 62
    FIELD_TYPE_BOOLEAN_ARRAY: ClassVar[Literal[63]] = 63
    FIELD_TYPE_BYTE_ARRAY: ClassVar[Literal[64]] = 64
    FIELD_TYPE_STRING_ARRAY: ClassVar[Literal[65]] = 65
    FIELD_TYPE_WSTRING_ARRAY: ClassVar[Literal[66]] = 66
    FIELD_TYPE_FIXED_STRING_ARRAY: ClassVar[Literal[67]] = 67
    FIELD_TYPE_FIXED_WSTRING_ARRAY: ClassVar[Literal[68]] = 68
    FIELD_TYPE_BOUNDED_STRING_ARRAY: ClassVar[Literal[69]] = 69
    FIELD_TYPE_BOUNDED_WSTRING_ARRAY: ClassVar[Literal[70]] = 70
    FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE: ClassVar[Literal[97]] = 97
    FIELD_TYPE_INT8_BOUNDED_SEQUENCE: ClassVar[Literal[98]] = 98
    FIELD_TYPE_UINT8_BOUNDED_SEQUENCE: ClassVar[Literal[99]] = 99
    FIELD_TYPE_INT16_BOUNDED_SEQUENCE: ClassVar[Literal[100]] = 100
    FIELD_TYPE_UINT16_BOUNDED_SEQUENCE: ClassVar[Literal[101]] = 101
    FIELD_TYPE_INT32_BOUNDED_SEQUENCE: ClassVar[Literal[102]] = 102
    FIELD_TYPE_UINT32_BOUNDED_SEQUENCE: ClassVar[Literal[103]] = 103
    FIELD_TYPE_INT64_BOUNDED_SEQUENCE: ClassVar[Literal[104]] = 104
    FIELD_TYPE_UINT64_BOUNDED_SEQUENCE: ClassVar[Literal[105]] = 105
    FIELD_TYPE_FLOAT_BOUNDED_SEQUENCE: ClassVar[Literal[106]] = 106
    FIELD_TYPE_DOUBLE_BOUNDED_SEQUENCE: ClassVar[Literal[107]] = 107
    FIELD_TYPE_LONG_DOUBLE_BOUNDED_SEQUENCE: ClassVar[Literal[108]] = 108
    FIELD_TYPE_CHAR_BOUNDED_SEQUENCE: ClassVar[Literal[109]] = 109
    FIELD_TYPE_WCHAR_BOUNDED_SEQUENCE: ClassVar[Literal[110]] = 110
    FIELD_TYPE_BOOLEAN_BOUNDED_SEQUENCE: ClassVar[Literal[111]] = 111
    FIELD_TYPE_BYTE_BOUNDED_SEQUENCE: ClassVar[Literal[112]] = 112
    FIELD_TYPE_STRING_BOUNDED_SEQUENCE: ClassVar[Literal[113]] = 113
    FIELD_TYPE_WSTRING_BOUNDED_SEQUENCE: ClassVar[Literal[114]] = 114
    FIELD_TYPE_FIXED_STRING_BOUNDED_SEQUENCE: ClassVar[Literal[115]] = 115
    FIELD_TYPE_FIXED_WSTRING_BOUNDED_SEQUENCE: ClassVar[Literal[116]] = 116
    FIELD_TYPE_BOUNDED_STRING_BOUNDED_SEQUENCE: ClassVar[Literal[117]] = 117
    FIELD_TYPE_BOUNDED_WSTRING_BOUNDED_SEQUENCE: ClassVar[Literal[118]] = 118
    FIELD_TYPE_NESTED_TYPE_UNBOUNDED_SEQUENCE: ClassVar[Literal[145]] = 145
    FIELD_TYPE_INT8_UNBOUNDED_SEQUENCE: ClassVar[Literal[146]] = 146
    FIELD_TYPE_UINT8_UNBOUNDED_SEQUENCE: ClassVar[Literal[147]] = 147
    FIELD_TYPE_INT16_UNBOUNDED_SEQUENCE: ClassVar[Literal[148]] = 148
    FIELD_TYPE_UINT16_UNBOUNDED_SEQUENCE: ClassVar[Literal[149]] = 149
    FIELD_TYPE_INT32_UNBOUNDED_SEQUENCE: ClassVar[Literal[150]] = 150
    FIELD_TYPE_UINT32_UNBOUNDED_SEQUENCE: ClassVar[Literal[151]] = 151
    FIELD_TYPE_INT64_UNBOUNDED_SEQUENCE: ClassVar[Literal[152]] = 152
    FIELD_TYPE_UINT64_UNBOUNDED_SEQUENCE: ClassVar[Literal[153]] = 153
    FIELD_TYPE_FLOAT_UNBOUNDED_SEQUENCE: ClassVar[Literal[154]] = 154
    FIELD_TYPE_DOUBLE_UNBOUNDED_SEQUENCE: ClassVar[Literal[155]] = 155
    FIELD_TYPE_LONG_DOUBLE_UNBOUNDED_SEQUENCE: ClassVar[Literal[156]] = 156
    FIELD_TYPE_CHAR_UNBOUNDED_SEQUENCE: ClassVar[Literal[157]] = 157
    FIELD_TYPE_WCHAR_UNBOUNDED_SEQUENCE: ClassVar[Literal[158]] = 158
    FIELD_TYPE_BOOLEAN_UNBOUNDED_SEQUENCE: ClassVar[Literal[159]] = 159
    FIELD_TYPE_BYTE_UNBOUNDED_SEQUENCE: ClassVar[Literal[160]] = 160
    FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE: ClassVar[Literal[161]] = 161
    FIELD_TYPE_WSTRING_UNBOUNDED_SEQUENCE: ClassVar[Literal[162]] = 162
    FIELD_TYPE_FIXED_STRING_UNBOUNDED_SEQUENCE: ClassVar[Literal[163]] = 163
    FIELD_TYPE_FIXED_WSTRING_UNBOUNDED_SEQUENCE: ClassVar[Literal[164]] = 164
    FIELD_TYPE_BOUNDED_STRING_UNBOUNDED_SEQUENCE: ClassVar[Literal[165]] = 165
    FIELD_TYPE_BOUNDED_WSTRING_UNBOUNDED_SEQUENCE: ClassVar[Literal[166]] = 166

    type_id: types.uint8 = 0
    capacity: types.uint64 = 0
    string_capacity: types.uint64 = 0
    nested_type_name: types.bounded_str[255] = ""


@dataclass
class Field(IdlStruct, typename="type_description_interfaces/msg/Field"):
    name: str = ""
    type: FieldType = field(default_factory=FieldType)
    default_value: str = ""


@dataclass
class IndividualTypeDescription(
    IdlStruct, typename="type_description_interfaces/msg/IndividualTypeDescription"
):
    type_name: types.bounded_str[255] = ""
    fields: types.sequence[Field] = field(default_factory=list)


@dataclass
class KeyValue(IdlStruct, typename="type_description_interfaces/msg/KeyValue"):
    key: str = ""
    value: str = ""


@dataclass
class TypeDescription(
    IdlStruct, typename="type_description_interfaces/msg/TypeDescription"
):
    type_description: IndividualTypeDescription = field(
        default_factory=IndividualTypeDescription
    )
    referenced_type_descriptions: types.sequence[IndividualTypeDescription] = field(
        default_factory=list
    )


@dataclass
class TypeSource(IdlStruct, typename="type_description_interfaces/msg/TypeSource"):
    type_name: str = ""
    encoding: str = ""
    raw_file_contents: str = ""

