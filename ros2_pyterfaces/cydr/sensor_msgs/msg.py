from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..builtin_interfaces.msg import Time
from ..geometry_msgs.msg import Point32, Quaternion, Transform, Twist, Vector3, Wrench
from ..idl import IdlStruct
from ..std_msgs.msg import Header


class BatteryState(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/BatteryState"
    header: Header = msgspec.field(default_factory=Header)
    voltage: types.float32 = np.float32(0.0)
    temperature: types.float32 = np.float32(0.0)
    current: types.float32 = np.float32(0.0)
    charge: types.float32 = np.float32(0.0)
    capacity: types.float32 = np.float32(0.0)
    design_capacity: types.float32 = np.float32(0.0)
    percentage: types.float32 = np.float32(0.0)
    power_supply_status: types.uint8 = np.uint8(0)
    power_supply_health: types.uint8 = np.uint8(0)
    power_supply_technology: types.uint8 = np.uint8(0)
    present: types.boolean = False
    cell_voltage: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )
    cell_temperature: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )
    location: types.string = b""
    serial_number: types.string = b""


class ChannelFloat32(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/ChannelFloat32"
    name: types.string = b""
    values: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )


class CompressedImage(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/CompressedImage"
    header: Header = msgspec.field(default_factory=Header)
    format: types.string = b""
    data: types.NDArray[Any, types.UInt8] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.uint8)
    )


class FluidPressure(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/FluidPressure"
    header: Header = msgspec.field(default_factory=Header)
    fluid_pressure: types.float64 = np.float64(0.0)
    variance: types.float64 = np.float64(0.0)


class Illuminance(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/Illuminance"
    header: Header = msgspec.field(default_factory=Header)
    illuminance: types.float64 = np.float64(0.0)
    variance: types.float64 = np.float64(0.0)


class Image(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/Image"
    header: Header = msgspec.field(default_factory=Header)
    height: types.uint32 = np.uint32(0)
    width: types.uint32 = np.uint32(0)
    encoding: types.string = b""
    is_bigendian: types.uint8 = np.uint8(0)
    step: types.uint32 = np.uint32(0)
    data: types.NDArray[Any, types.UInt8] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.uint8)
    )


class Imu(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/Imu"
    header: Header = msgspec.field(default_factory=Header)
    orientation: Quaternion = msgspec.field(default_factory=Quaternion)
    orientation_covariance: types.NDArray[types.Shape["9"], types.Float64] = (
        msgspec.field(
            default_factory=lambda: np.array(
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
            )
        )
    )
    angular_velocity: Vector3 = msgspec.field(default_factory=Vector3)
    angular_velocity_covariance: types.NDArray[types.Shape["9"], types.Float64] = (
        msgspec.field(
            default_factory=lambda: np.array(
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
            )
        )
    )
    linear_acceleration: Vector3 = msgspec.field(default_factory=Vector3)
    linear_acceleration_covariance: types.NDArray[types.Shape["9"], types.Float64] = (
        msgspec.field(
            default_factory=lambda: np.array(
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
            )
        )
    )


class JointState(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/JointState"
    header: Header = msgspec.field(default_factory=Header)
    name: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )
    position: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )
    velocity: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )
    effort: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )


class Joy(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/Joy"
    header: Header = msgspec.field(default_factory=Header)
    axes: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )
    buttons: types.NDArray[Any, types.Int32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.int32)
    )


class JoyFeedback(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/JoyFeedback"
    type: types.uint8 = np.uint8(0)
    id: types.uint8 = np.uint8(0)
    intensity: types.float32 = np.float32(0.0)


class LaserEcho(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/LaserEcho"
    echoes: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )


class LaserScan(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/LaserScan"
    header: Header = msgspec.field(default_factory=Header)
    angle_min: types.float32 = np.float32(0.0)
    angle_max: types.float32 = np.float32(0.0)
    angle_increment: types.float32 = np.float32(0.0)
    time_increment: types.float32 = np.float32(0.0)
    scan_time: types.float32 = np.float32(0.0)
    range_min: types.float32 = np.float32(0.0)
    range_max: types.float32 = np.float32(0.0)
    ranges: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )
    intensities: types.NDArray[Any, types.Float32] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float32)
    )


class MagneticField(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/MagneticField"
    header: Header = msgspec.field(default_factory=Header)
    magnetic_field: Vector3 = msgspec.field(default_factory=Vector3)
    magnetic_field_covariance: types.NDArray[types.Shape["9"], types.Float64] = (
        msgspec.field(
            default_factory=lambda: np.array(
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
            )
        )
    )


class MultiDOFJointState(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/MultiDOFJointState"
    __unsupported_reason__ = (
        "transforms is a collection of messages, which cydr does not support"
    )
    pass


class NavSatStatus(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/NavSatStatus"
    status: types.int8 = np.int8(-2)
    service: types.uint16 = np.uint16(0)


class PointField(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/PointField"
    name: types.string = b""
    offset: types.uint32 = np.uint32(0)
    datatype: types.uint8 = np.uint8(0)
    count: types.uint32 = np.uint32(0)


class Range(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/Range"
    header: Header = msgspec.field(default_factory=Header)
    radiation_type: types.uint8 = np.uint8(0)
    field_of_view: types.float32 = np.float32(0.0)
    min_range: types.float32 = np.float32(0.0)
    max_range: types.float32 = np.float32(0.0)
    range: types.float32 = np.float32(0.0)
    variance: types.float32 = np.float32(0.0)


class RegionOfInterest(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/RegionOfInterest"
    x_offset: types.uint32 = np.uint32(0)
    y_offset: types.uint32 = np.uint32(0)
    height: types.uint32 = np.uint32(0)
    width: types.uint32 = np.uint32(0)
    do_rectify: types.boolean = False


class RelativeHumidity(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/RelativeHumidity"
    header: Header = msgspec.field(default_factory=Header)
    relative_humidity: types.float64 = np.float64(0.0)
    variance: types.float64 = np.float64(0.0)


class Temperature(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/Temperature"
    header: Header = msgspec.field(default_factory=Header)
    temperature: types.float64 = np.float64(0.0)
    variance: types.float64 = np.float64(0.0)


class TimeReference(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/TimeReference"
    header: Header = msgspec.field(default_factory=Header)
    time_ref: Time = msgspec.field(default_factory=Time)
    source: types.string = b""


class CameraInfo(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/CameraInfo"
    header: Header = msgspec.field(default_factory=Header)
    height: types.uint32 = np.uint32(0)
    width: types.uint32 = np.uint32(0)
    distortion_model: types.string = b""
    d: types.NDArray[Any, types.Float64] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.float64)
    )
    k: types.NDArray[types.Shape["9"], types.Float64] = msgspec.field(
        default_factory=lambda: np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
        )
    )
    r: types.NDArray[types.Shape["9"], types.Float64] = msgspec.field(
        default_factory=lambda: np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
        )
    )
    p: types.NDArray[types.Shape["12"], types.Float64] = msgspec.field(
        default_factory=lambda: np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            dtype=np.float64,
        )
    )
    binning_x: types.uint32 = np.uint32(0)
    binning_y: types.uint32 = np.uint32(0)
    roi: RegionOfInterest = msgspec.field(default_factory=RegionOfInterest)


class JoyFeedbackArray(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/JoyFeedbackArray"
    __unsupported_reason__ = (
        "array is a collection of messages, which cydr does not support"
    )
    pass


class MultiEchoLaserScan(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/MultiEchoLaserScan"
    __unsupported_reason__ = (
        "ranges is a collection of messages, which cydr does not support"
    )
    pass


class NavSatFix(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/NavSatFix"
    header: Header = msgspec.field(default_factory=Header)
    status: NavSatStatus = msgspec.field(default_factory=NavSatStatus)
    latitude: types.float64 = np.float64(0.0)
    longitude: types.float64 = np.float64(0.0)
    altitude: types.float64 = np.float64(0.0)
    position_covariance: types.NDArray[types.Shape["9"], types.Float64] = msgspec.field(
        default_factory=lambda: np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64
        )
    )
    position_covariance_type: types.uint8 = np.uint8(0)


class PointCloud(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/PointCloud"
    __unsupported_reason__ = (
        "points is a collection of messages, which cydr does not support"
    )
    pass


class PointCloud2(IdlStruct):
    __idl_typename__ = "sensor_msgs/msg/PointCloud2"
    __unsupported_reason__ = (
        "fields is a collection of messages, which cydr does not support"
    )
    pass
