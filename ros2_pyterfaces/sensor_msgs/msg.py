from dataclasses import dataclass, field
from typing import ClassVar, Literal

import numpy as np

from .. import DISTRO, Distro
from ..builtin_interfaces.msg import Time
from ..geometry_msgs.msg import Point32, Quaternion, Transform, Twist, Vector3, Wrench
from ..idl import IdlStruct, types
from ..std_msgs.msg import Header


@dataclass
class BatteryState(IdlStruct, typename="sensor_msgs/msg/BatteryState"):
    POWER_SUPPLY_STATUS_UNKNOWN: ClassVar[Literal[0]] = 0
    POWER_SUPPLY_STATUS_CHARGING: ClassVar[Literal[1]] = 1
    POWER_SUPPLY_STATUS_DISCHARGING: ClassVar[Literal[2]] = 2
    POWER_SUPPLY_STATUS_NOT_CHARGING: ClassVar[Literal[3]] = 3
    POWER_SUPPLY_STATUS_FULL: ClassVar[Literal[4]] = 4
    POWER_SUPPLY_HEALTH_UNKNOWN: ClassVar[Literal[0]] = 0
    POWER_SUPPLY_HEALTH_GOOD: ClassVar[Literal[1]] = 1
    POWER_SUPPLY_HEALTH_OVERHEAT: ClassVar[Literal[2]] = 2
    POWER_SUPPLY_HEALTH_DEAD: ClassVar[Literal[3]] = 3
    POWER_SUPPLY_HEALTH_OVERVOLTAGE: ClassVar[Literal[4]] = 4
    POWER_SUPPLY_HEALTH_UNSPEC_FAILURE: ClassVar[Literal[5]] = 5
    POWER_SUPPLY_HEALTH_COLD: ClassVar[Literal[6]] = 6
    POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE: ClassVar[Literal[7]] = 7
    POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE: ClassVar[Literal[8]] = 8
    POWER_SUPPLY_TECHNOLOGY_UNKNOWN: ClassVar[Literal[0]] = 0
    POWER_SUPPLY_TECHNOLOGY_NIMH: ClassVar[Literal[1]] = 1
    POWER_SUPPLY_TECHNOLOGY_LION: ClassVar[Literal[2]] = 2
    POWER_SUPPLY_TECHNOLOGY_LIPO: ClassVar[Literal[3]] = 3
    POWER_SUPPLY_TECHNOLOGY_LIFE: ClassVar[Literal[4]] = 4
    POWER_SUPPLY_TECHNOLOGY_NICD: ClassVar[Literal[5]] = 5
    POWER_SUPPLY_TECHNOLOGY_LIMN: ClassVar[Literal[6]] = 6
    POWER_SUPPLY_TECHNOLOGY_TERNARY: ClassVar[Literal[7]] = 7
    POWER_SUPPLY_TECHNOLOGY_VRLA: ClassVar[Literal[8]] = 8
    header: Header = field(default_factory=Header)
    voltage: types.float32 = 0.0
    temperature: types.float32 = 0.0
    current: types.float32 = 0.0
    charge: types.float32 = 0.0
    capacity: types.float32 = 0.0
    design_capacity: types.float32 = 0.0
    percentage: types.float32 = 0.0
    power_supply_status: types.uint8 = 0
    power_supply_health: types.uint8 = 0
    power_supply_technology: types.uint8 = 0
    present: bool = False
    cell_voltage: types.sequence[types.float32] = field(default_factory=list)
    cell_temperature: types.sequence[types.float32] = field(default_factory=list)
    location: str = ""
    serial_number: str = ""


@dataclass
class ChannelFloat32(IdlStruct, typename="sensor_msgs/msg/ChannelFloat32"):
    name: str = ""
    values: types.sequence[types.float32] = field(default_factory=list)


@dataclass
class CompressedImage(IdlStruct, typename="sensor_msgs/msg/CompressedImage"):
    header: Header = field(default_factory=Header)
    format: str = ""
    data: types.sequence[types.uint8] = field(default_factory=list)


@dataclass
class FluidPressure(IdlStruct, typename="sensor_msgs/msg/FluidPressure"):
    header: Header = field(default_factory=Header)
    fluid_pressure: types.float64 = 0.0
    variance: types.float64 = 0.0


@dataclass
class Illuminance(IdlStruct, typename="sensor_msgs/msg/Illuminance"):
    header: Header = field(default_factory=Header)
    illuminance: types.float64 = 0.0
    variance: types.float64 = 0.0


@dataclass
class Image(IdlStruct, typename="sensor_msgs/msg/Image"):
    header: Header = field(default_factory=Header)
    height: types.uint32 = 0
    width: types.uint32 = 0
    encoding: str = ""
    is_bigendian: types.uint8 = 0
    step: types.uint32 = 0
    data: types.sequence[types.uint8] = field(default_factory=list)


@dataclass
class Imu(IdlStruct, typename="sensor_msgs/msg/Imu"):
    header: Header = field(default_factory=Header)
    orientation: Quaternion = field(default_factory=Quaternion)
    orientation_covariance: types.array[types.float64, 9] = field(
        default_factory=lambda: np.zeros(9)
    )
    angular_velocity: Vector3 = field(default_factory=Vector3)
    angular_velocity_covariance: types.array[types.float64, 9] = field(
        default_factory=lambda: np.zeros(9)
    )
    linear_acceleration: Vector3 = field(default_factory=Vector3)
    linear_acceleration_covariance: types.array[types.float64, 9] = field(
        default_factory=lambda: np.zeros(9)
    )


@dataclass
class JointState(IdlStruct, typename="sensor_msgs/msg/JointState"):
    header: Header = field(default_factory=Header)
    name: types.sequence[str] = field(default_factory=list)
    position: types.sequence[types.float64] = field(default_factory=list)
    velocity: types.sequence[types.float64] = field(default_factory=list)
    effort: types.sequence[types.float64] = field(default_factory=list)


@dataclass
class Joy(IdlStruct, typename="sensor_msgs/msg/Joy"):
    header: Header = field(default_factory=Header)
    axes: types.sequence[types.float32] = field(default_factory=list)
    buttons: types.sequence[types.int32] = field(default_factory=list)


@dataclass
class JoyFeedback(IdlStruct, typename="sensor_msgs/msg/JoyFeedback"):
    TYPE_LED: ClassVar[Literal[0]] = 0
    TYPE_RUMBLE: ClassVar[Literal[1]] = 1
    TYPE_BUZZER: ClassVar[Literal[2]] = 2
    type: types.uint8 = 0
    id: types.uint8 = 0
    intensity: types.float32 = 0.0


@dataclass
class LaserEcho(IdlStruct, typename="sensor_msgs/msg/LaserEcho"):
    echoes: types.sequence[types.float32] = field(default_factory=list)


@dataclass
class LaserScan(IdlStruct, typename="sensor_msgs/msg/LaserScan"):
    header: Header = field(default_factory=Header)
    angle_min: types.float32 = 0.0
    angle_max: types.float32 = 0.0
    angle_increment: types.float32 = 0.0
    time_increment: types.float32 = 0.0
    scan_time: types.float32 = 0.0
    range_min: types.float32 = 0.0
    range_max: types.float32 = 0.0
    ranges: types.sequence[types.float32] = field(default_factory=list)
    intensities: types.sequence[types.float32] = field(default_factory=list)


@dataclass
class MagneticField(IdlStruct, typename="sensor_msgs/msg/MagneticField"):
    header: Header = field(default_factory=Header)
    magnetic_field: Vector3 = field(default_factory=Vector3)
    magnetic_field_covariance: types.array[types.float64, 9] = field(
        default_factory=lambda: np.zeros(9)
    )


@dataclass
class MultiDOFJointState(IdlStruct, typename="sensor_msgs/msg/MultiDOFJointState"):
    header: Header = field(default_factory=Header)
    joint_names: types.sequence[str] = field(default_factory=list)
    transforms: types.sequence[Transform] = field(default_factory=list)
    twist: types.sequence[Twist] = field(default_factory=list)
    wrench: types.sequence[Wrench] = field(default_factory=list)


@dataclass
class NavSatStatus(IdlStruct, typename="sensor_msgs/msg/NavSatStatus"):
    STATUS_UNKNOWN: ClassVar[Literal[-2]] = -2
    STATUS_NO_FIX: ClassVar[Literal[-1]] = -1
    STATUS_FIX: ClassVar[Literal[0]] = 0
    STATUS_SBAS_FIX: ClassVar[Literal[1]] = 1
    STATUS_GBAS_FIX: ClassVar[Literal[2]] = 2
    SERVICE_UNKNOWN: ClassVar[Literal[0]] = 0
    SERVICE_GPS: ClassVar[Literal[1]] = 1
    SERVICE_GLONASS: ClassVar[Literal[2]] = 2
    SERVICE_COMPASS: ClassVar[Literal[4]] = 4
    SERVICE_GALILEO: ClassVar[Literal[8]] = 8
    status: types.int8 = 0 if DISTRO == Distro.HUMBLE else -2
    service: types.uint16 = 0


@dataclass
class PointField(IdlStruct, typename="sensor_msgs/msg/PointField"):
    INT8: ClassVar[Literal[1]] = 1
    UINT8: ClassVar[Literal[2]] = 2
    INT16: ClassVar[Literal[3]] = 3
    UINT16: ClassVar[Literal[4]] = 4
    INT32: ClassVar[Literal[5]] = 5
    UINT32: ClassVar[Literal[6]] = 6
    FLOAT32: ClassVar[Literal[7]] = 7
    FLOAT64: ClassVar[Literal[8]] = 8
    INT64: ClassVar[Literal[9]] = 9
    UINT64: ClassVar[Literal[10]] = 10
    BOOL: ClassVar[Literal[11]] = 11
    name: str = ""
    offset: types.uint32 = 0
    datatype: types.uint8 = 0
    count: types.uint32 = 0

@dataclass
class Range(IdlStruct, typename="sensor_msgs/msg/Range"):
    ULTRASOUND: ClassVar[Literal[0]] = 0
    INFRARED: ClassVar[Literal[1]] = 1
    header: Header = field(default_factory=Header)
    radiation_type: types.uint8 = 0
    field_of_view: types.float32 = 0.0
    min_range: types.float32 = 0.0
    max_range: types.float32 = 0.0
    range: types.float32 = 0.0
    variance: types.float32 = 0.0


if DISTRO == Distro.HUMBLE:
    # overide for humble

    @dataclass
    class RangeHumble(IdlStruct, typename="sensor_msgs/msg/Range"):
        ULTRASOUND: ClassVar[Literal[0]] = 0
        INFRARED: ClassVar[Literal[1]] = 1
        header: Header = field(default_factory=Header)
        radiation_type: types.uint8 = 0
        field_of_view: types.float32 = 0.0
        min_range: types.float32 = 0.0
        max_range: types.float32 = 0.0
        range: types.float32 = 0.0

    Range = RangeHumble # type: ignore


@dataclass
class RegionOfInterest(IdlStruct, typename="sensor_msgs/msg/RegionOfInterest"):
    x_offset: types.uint32 = 0
    y_offset: types.uint32 = 0
    height: types.uint32 = 0
    width: types.uint32 = 0
    do_rectify: bool = False


@dataclass
class RelativeHumidity(IdlStruct, typename="sensor_msgs/msg/RelativeHumidity"):
    header: Header = field(default_factory=Header)
    relative_humidity: types.float64 = 0.0
    variance: types.float64 = 0.0


@dataclass
class Temperature(IdlStruct, typename="sensor_msgs/msg/Temperature"):
    header: Header = field(default_factory=Header)
    temperature: types.float64 = 0.0
    variance: types.float64 = 0.0


@dataclass
class TimeReference(IdlStruct, typename="sensor_msgs/msg/TimeReference"):
    header: Header = field(default_factory=Header)
    time_ref: Time = field(default_factory=Time)
    source: str = ""


@dataclass
class CameraInfo(IdlStruct, typename="sensor_msgs/msg/CameraInfo"):
    header: Header = field(default_factory=Header)
    height: types.uint32 = 0
    width: types.uint32 = 0
    distortion_model: str = ""
    d: types.sequence[types.float64] = field(default_factory=list)
    k: types.array[types.float64, 9] = field(default_factory=lambda: np.zeros(9))
    r: types.array[types.float64, 9] = field(default_factory=lambda: np.zeros(9))
    p: types.array[types.float64, 12] = field(default_factory=lambda: np.zeros(12))
    binning_x: types.uint32 = 0
    binning_y: types.uint32 = 0
    roi: RegionOfInterest = field(default_factory=RegionOfInterest)


@dataclass
class JoyFeedbackArray(IdlStruct, typename="sensor_msgs/msg/JoyFeedbackArray"):
    array: types.sequence[JoyFeedback] = field(default_factory=list)


@dataclass
class MultiEchoLaserScan(IdlStruct, typename="sensor_msgs/msg/MultiEchoLaserScan"):
    header: Header = field(default_factory=Header)
    angle_min: types.float32 = 0.0
    angle_max: types.float32 = 0.0
    angle_increment: types.float32 = 0.0
    time_increment: types.float32 = 0.0
    scan_time: types.float32 = 0.0
    range_min: types.float32 = 0.0
    range_max: types.float32 = 0.0
    ranges: types.sequence[LaserEcho] = field(default_factory=list)
    intensities: types.sequence[LaserEcho] = field(default_factory=list)


@dataclass
class NavSatFix(IdlStruct, typename="sensor_msgs/msg/NavSatFix"):
    COVARIANCE_TYPE_UNKNOWN: ClassVar[Literal[0]] = 0
    COVARIANCE_TYPE_APPROXIMATED: ClassVar[Literal[1]] = 1
    COVARIANCE_TYPE_DIAGONAL_KNOWN: ClassVar[Literal[2]] = 2
    COVARIANCE_TYPE_KNOWN: ClassVar[Literal[3]] = 3
    header: Header = field(default_factory=Header)
    status: NavSatStatus = field(default_factory=NavSatStatus)
    latitude: types.float64 = 0.0
    longitude: types.float64 = 0.0
    altitude: types.float64 = 0.0
    position_covariance: types.array[types.float64, 9] = field(
        default_factory=lambda: np.zeros(9)
    )
    position_covariance_type: types.uint8 = 0


@dataclass
class PointCloud(IdlStruct, typename="sensor_msgs/msg/PointCloud"):
    header: Header = field(default_factory=Header)
    points: types.sequence[Point32] = field(default_factory=list)
    channels: types.sequence[ChannelFloat32] = field(default_factory=list)


@dataclass
class PointCloud2(IdlStruct, typename="sensor_msgs/msg/PointCloud2"):
    header: Header = field(default_factory=Header)
    height: types.uint32 = 0
    width: types.uint32 = 0
    fields: types.sequence[PointField] = field(default_factory=list)
    is_bigendian: bool = False
    point_step: types.uint32 = 0
    row_step: types.uint32 = 0
    data: types.sequence[types.uint8] = field(default_factory=list)
    is_dense: bool = False
