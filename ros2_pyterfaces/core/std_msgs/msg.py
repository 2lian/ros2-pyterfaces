from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time

Bool: CoreSchema = {
    "__typename": "std_msgs/msg/Bool",
    "data": "bool",
}

Byte: CoreSchema = {
    "__typename": "std_msgs/msg/Byte",
    "data": "byte",
}

Char: CoreSchema = {
    "__typename": "std_msgs/msg/Char",
    "data": "uint8",
}

ColorRGBA: CoreSchema = {
    "__typename": "std_msgs/msg/ColorRGBA",
    "r": "float32",
    "g": "float32",
    "b": "float32",
    "a": "float32",
}

Empty: CoreSchema = {
    "__typename": "std_msgs/msg/Empty",
}

Float32: CoreSchema = {
    "__typename": "std_msgs/msg/Float32",
    "data": "float32",
}

Float64: CoreSchema = {
    "__typename": "std_msgs/msg/Float64",
    "data": "float64",
}

Header: CoreSchema = {
    "__typename": "std_msgs/msg/Header",
    "stamp": Time,
    "frame_id": "string",
}

Int16: CoreSchema = {
    "__typename": "std_msgs/msg/Int16",
    "data": "int16",
}

Int32: CoreSchema = {
    "__typename": "std_msgs/msg/Int32",
    "data": "int32",
}

Int64: CoreSchema = {
    "__typename": "std_msgs/msg/Int64",
    "data": "int64",
}

Int8: CoreSchema = {
    "__typename": "std_msgs/msg/Int8",
    "data": "int8",
}

MultiArrayDimension: CoreSchema = {
    "__typename": "std_msgs/msg/MultiArrayDimension",
    "label": "string",
    "size": "uint32",
    "stride": "uint32",
}

String: CoreSchema = {
    "__typename": "std_msgs/msg/String",
    "data": "string",
}

UInt16: CoreSchema = {
    "__typename": "std_msgs/msg/UInt16",
    "data": "uint16",
}

UInt32: CoreSchema = {
    "__typename": "std_msgs/msg/UInt32",
    "data": "uint32",
}

UInt64: CoreSchema = {
    "__typename": "std_msgs/msg/UInt64",
    "data": "uint64",
}

UInt8: CoreSchema = {
    "__typename": "std_msgs/msg/UInt8",
    "data": "uint8",
}

MultiArrayLayout: CoreSchema = {
    "__typename": "std_msgs/msg/MultiArrayLayout",
    "dim": Sequence(MultiArrayDimension),
    "data_offset": "uint32",
}

ByteMultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/ByteMultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("byte"),
}

Float32MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/Float32MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("float32"),
}

Float64MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/Float64MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("float64"),
}

Int16MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/Int16MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("int16"),
}

Int32MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/Int32MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("int32"),
}

Int64MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/Int64MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("int64"),
}

Int8MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/Int8MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("int8"),
}

UInt16MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/UInt16MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("uint16"),
}

UInt32MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/UInt32MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("uint32"),
}

UInt64MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/UInt64MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("uint64"),
}

UInt8MultiArray: CoreSchema = {
    "__typename": "std_msgs/msg/UInt8MultiArray",
    "layout": MultiArrayLayout,
    "data": Sequence("uint8"),
}

__all__ = [
    "Bool",
    "Byte",
    "Char",
    "ColorRGBA",
    "Empty",
    "Float32",
    "Float64",
    "Header",
    "Int16",
    "Int32",
    "Int64",
    "Int8",
    "MultiArrayDimension",
    "String",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt8",
    "MultiArrayLayout",
    "ByteMultiArray",
    "Float32MultiArray",
    "Float64MultiArray",
    "Int16MultiArray",
    "Int32MultiArray",
    "Int64MultiArray",
    "Int8MultiArray",
    "UInt16MultiArray",
    "UInt32MultiArray",
    "UInt64MultiArray",
    "UInt8MultiArray",
]
