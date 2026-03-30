from dataclasses import dataclass, field

from ..builtin_interfaces.msg import Time
from ..idl import IdlStruct, types


@dataclass
class Bool(IdlStruct, typename="std_msgs/msg/Bool"):
    data: bool = False


@dataclass
class Byte(IdlStruct, typename="std_msgs/msg/Byte"):
    data: types.byte = 0


@dataclass
class Char(IdlStruct, typename="std_msgs/msg/Char"):
    # type_description_interfaces.srv.GetTypeDescription_Response(
    #     successful=True,
    #     failure_reason="",
    #     type_description=type_description_interfaces.msg.TypeDescription(
    #         type_description=type_description_interfaces.msg.IndividualTypeDescription(
    #             type_name="std_msgs/msg/Char",
    #             fields=[
    #                 type_description_interfaces.msg.Field(
    #                     name="data",
    #                     type=type_description_interfaces.msg.FieldType(
    #                         type_id=3,
    #                         capacity=0,
    #                         string_capacity=0,
    #                         nested_type_name="",
    #                     ),
    #                     default_value="",
    #                 )
    #             ],
    #         ),
    #         referenced_type_descriptions=[],
    #     ),
    #     type_sources=[
    #         type_description_interfaces.msg.TypeSource(
    #             type_name="std_msgs/msg/Char",
    #             encoding="msg",
    #             raw_file_contents="# This was originally provided as an example message.\n# It is deprecated as of Foxy\n# It is recommended to create your own semantically meaningful message.\n# However if you would like to continue using this please use the equivalent in example_msgs.\n\nchar data",
    #         )
    #     ],
    #     extra_information=[],
    # )
    data: types.uint8 = 0


@dataclass
class ColorRGBA(IdlStruct, typename="std_msgs/msg/ColorRGBA"):
    r: types.float32 = 0.0
    g: types.float32 = 0.0
    b: types.float32 = 0.0
    a: types.float32 = 0.0


@dataclass
class Empty(IdlStruct, typename="std_msgs/msg/Empty"):
    # type_description_interfaces.srv.GetTypeDescription_Response(
    #     successful=True,
    #     failure_reason="",
    #     type_description=type_description_interfaces.msg.TypeDescription(
    #         type_description=type_description_interfaces.msg.IndividualTypeDescription(
    #             type_name="std_msgs/msg/Empty",
    #             fields=[
    #                 type_description_interfaces.msg.Field(
    #                     name="structure_needs_at_least_one_member",
    #                     type=type_description_interfaces.msg.FieldType(
    #                         type_id=3,
    #                         capacity=0,
    #                         string_capacity=0,
    #                         nested_type_name="",
    #                     ),
    #                     default_value="",
    #                 )
    #             ],
    #         ),
    #         referenced_type_descriptions=[],
    #     ),
    #     type_sources=[
    #         type_description_interfaces.msg.TypeSource(
    #             type_name="std_msgs/msg/Empty", encoding="msg", raw_file_contents=""
    #         )
    #     ],
    #     extra_information=[],
    # )
    # structure_needs_at_least_one_member: types.uint8 = 0
    pass

@dataclass
class Float32(IdlStruct, typename="std_msgs/msg/Float32"):
    data: types.float32 = 0.0


@dataclass
class Float64(IdlStruct, typename="std_msgs/msg/Float64"):
    data: types.float64 = 0.0


@dataclass
class Header(IdlStruct, typename="std_msgs/msg/Header"):
    stamp: Time = field(default_factory=Time)
    frame_id: str = ""


@dataclass
class Int16(IdlStruct, typename="std_msgs/msg/Int16"):
    data: types.int16 = 0


@dataclass
class Int32(IdlStruct, typename="std_msgs/msg/Int32"):
    data: types.int32 = 0


@dataclass
class Int64(IdlStruct, typename="std_msgs/msg/Int64"):
    data: types.int64 = 0


@dataclass
class Int8(IdlStruct, typename="std_msgs/msg/Int8"):
    data: types.int8 = 0


@dataclass
class MultiArrayDimension(IdlStruct, typename="std_msgs/msg/MultiArrayDimension"):
    label: str = ""
    size: types.uint32 = 0
    stride: types.uint32 = 0


@dataclass
class String(IdlStruct, typename="std_msgs/msg/String"):
    data: str = ""


@dataclass
class UInt16(IdlStruct, typename="std_msgs/msg/UInt16"):
    data: types.uint16 = 0


@dataclass
class UInt32(IdlStruct, typename="std_msgs/msg/UInt32"):
    data: types.uint32 = 0


@dataclass
class UInt64(IdlStruct, typename="std_msgs/msg/UInt64"):
    data: types.uint64 = 0


@dataclass
class UInt8(IdlStruct, typename="std_msgs/msg/UInt8"):
    data: types.uint8 = 0


@dataclass
class MultiArrayLayout(IdlStruct, typename="std_msgs/msg/MultiArrayLayout"):
    dim: types.sequence[MultiArrayDimension] = field(default_factory=list)
    data_offset: types.uint32 = 0


@dataclass
class ByteMultiArray(IdlStruct, typename="std_msgs/msg/ByteMultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.byte] = field(default_factory=list)


@dataclass
class Float32MultiArray(IdlStruct, typename="std_msgs/msg/Float32MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.float32] = field(default_factory=list)


@dataclass
class Float64MultiArray(IdlStruct, typename="std_msgs/msg/Float64MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.float64] = field(default_factory=list)


@dataclass
class Int16MultiArray(IdlStruct, typename="std_msgs/msg/Int16MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.int16] = field(default_factory=list)


@dataclass
class Int32MultiArray(IdlStruct, typename="std_msgs/msg/Int32MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.int32] = field(default_factory=list)


@dataclass
class Int64MultiArray(IdlStruct, typename="std_msgs/msg/Int64MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.int64] = field(default_factory=list)


@dataclass
class Int8MultiArray(IdlStruct, typename="std_msgs/msg/Int8MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.int8] = field(default_factory=list)


@dataclass
class UInt16MultiArray(IdlStruct, typename="std_msgs/msg/UInt16MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.uint16] = field(default_factory=list)


@dataclass
class UInt32MultiArray(IdlStruct, typename="std_msgs/msg/UInt32MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.uint32] = field(default_factory=list)


@dataclass
class UInt64MultiArray(IdlStruct, typename="std_msgs/msg/UInt64MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.uint64] = field(default_factory=list)


@dataclass
class UInt8MultiArray(IdlStruct, typename="std_msgs/msg/UInt8MultiArray"):
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: types.sequence[types.uint8] = field(default_factory=list)
