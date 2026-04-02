from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time
from ..geometry_msgs.msg import Point32, Quaternion, Transform, Twist, Vector3, Wrench
from ..std_msgs.msg import Header

BatteryState: CoreSchema = {
    "__typename": "sensor_msgs/msg/BatteryState",
    "header": Header,
    "voltage": "float32",
    "temperature": "float32",
    "current": "float32",
    "charge": "float32",
    "capacity": "float32",
    "design_capacity": "float32",
    "percentage": "float32",
    "power_supply_status": "uint8",
    "power_supply_health": "uint8",
    "power_supply_technology": "uint8",
    "present": "bool",
    "cell_voltage": Sequence("float32"),
    "cell_temperature": Sequence("float32"),
    "location": "string",
    "serial_number": "string",
}

ChannelFloat32: CoreSchema = {
    "__typename": "sensor_msgs/msg/ChannelFloat32",
    "name": "string",
    "values": Sequence("float32"),
}

CompressedImage: CoreSchema = {
    "__typename": "sensor_msgs/msg/CompressedImage",
    "header": Header,
    "format": "string",
    "data": Sequence("uint8"),
}

FluidPressure: CoreSchema = {
    "__typename": "sensor_msgs/msg/FluidPressure",
    "header": Header,
    "fluid_pressure": "float64",
    "variance": "float64",
}

Illuminance: CoreSchema = {
    "__typename": "sensor_msgs/msg/Illuminance",
    "header": Header,
    "illuminance": "float64",
    "variance": "float64",
}

Image: CoreSchema = {
    "__typename": "sensor_msgs/msg/Image",
    "header": Header,
    "height": "uint32",
    "width": "uint32",
    "encoding": "string",
    "is_bigendian": "uint8",
    "step": "uint32",
    "data": Sequence("uint8"),
}

Imu: CoreSchema = {
    "__typename": "sensor_msgs/msg/Imu",
    "header": Header,
    "orientation": Quaternion,
    "orientation_covariance": Array("float64", 9),
    "angular_velocity": Vector3,
    "angular_velocity_covariance": Array("float64", 9),
    "linear_acceleration": Vector3,
    "linear_acceleration_covariance": Array("float64", 9),
}

JointState: CoreSchema = {
    "__typename": "sensor_msgs/msg/JointState",
    "header": Header,
    "name": Sequence("string"),
    "position": Sequence("float64"),
    "velocity": Sequence("float64"),
    "effort": Sequence("float64"),
}

Joy: CoreSchema = {
    "__typename": "sensor_msgs/msg/Joy",
    "header": Header,
    "axes": Sequence("float32"),
    "buttons": Sequence("int32"),
}

JoyFeedback: CoreSchema = {
    "__typename": "sensor_msgs/msg/JoyFeedback",
    "type": "uint8",
    "id": "uint8",
    "intensity": "float32",
}

LaserEcho: CoreSchema = {
    "__typename": "sensor_msgs/msg/LaserEcho",
    "echoes": Sequence("float32"),
}

LaserScan: CoreSchema = {
    "__typename": "sensor_msgs/msg/LaserScan",
    "header": Header,
    "angle_min": "float32",
    "angle_max": "float32",
    "angle_increment": "float32",
    "time_increment": "float32",
    "scan_time": "float32",
    "range_min": "float32",
    "range_max": "float32",
    "ranges": Sequence("float32"),
    "intensities": Sequence("float32"),
}

MagneticField: CoreSchema = {
    "__typename": "sensor_msgs/msg/MagneticField",
    "header": Header,
    "magnetic_field": Vector3,
    "magnetic_field_covariance": Array("float64", 9),
}

MultiDOFJointState: CoreSchema = {
    "__typename": "sensor_msgs/msg/MultiDOFJointState",
    "header": Header,
    "joint_names": Sequence("string"),
    "transforms": Sequence(Transform),
    "twist": Sequence(Twist),
    "wrench": Sequence(Wrench),
}

NavSatStatus: CoreSchema = {
    "__typename": "sensor_msgs/msg/NavSatStatus",
    "status": "int8",
    "service": "uint16",
}

PointField: CoreSchema = {
    "__typename": "sensor_msgs/msg/PointField",
    "name": "string",
    "offset": "uint32",
    "datatype": "uint8",
    "count": "uint32",
}

Range: CoreSchema = {
    "__typename": "sensor_msgs/msg/Range",
    "header": Header,
    "radiation_type": "uint8",
    "field_of_view": "float32",
    "min_range": "float32",
    "max_range": "float32",
    "range": "float32",
    "variance": "float32",
}

RegionOfInterest: CoreSchema = {
    "__typename": "sensor_msgs/msg/RegionOfInterest",
    "x_offset": "uint32",
    "y_offset": "uint32",
    "height": "uint32",
    "width": "uint32",
    "do_rectify": "bool",
}

RelativeHumidity: CoreSchema = {
    "__typename": "sensor_msgs/msg/RelativeHumidity",
    "header": Header,
    "relative_humidity": "float64",
    "variance": "float64",
}

Temperature: CoreSchema = {
    "__typename": "sensor_msgs/msg/Temperature",
    "header": Header,
    "temperature": "float64",
    "variance": "float64",
}

TimeReference: CoreSchema = {
    "__typename": "sensor_msgs/msg/TimeReference",
    "header": Header,
    "time_ref": Time,
    "source": "string",
}

PointCloud: CoreSchema = {
    "__typename": "sensor_msgs/msg/PointCloud",
    "header": Header,
    "points": Sequence(Point32),
    "channels": Sequence(ChannelFloat32),
}

JoyFeedbackArray: CoreSchema = {
    "__typename": "sensor_msgs/msg/JoyFeedbackArray",
    "array": Sequence(JoyFeedback),
}

MultiEchoLaserScan: CoreSchema = {
    "__typename": "sensor_msgs/msg/MultiEchoLaserScan",
    "header": Header,
    "angle_min": "float32",
    "angle_max": "float32",
    "angle_increment": "float32",
    "time_increment": "float32",
    "scan_time": "float32",
    "range_min": "float32",
    "range_max": "float32",
    "ranges": Sequence(LaserEcho),
    "intensities": Sequence(LaserEcho),
}

NavSatFix: CoreSchema = {
    "__typename": "sensor_msgs/msg/NavSatFix",
    "header": Header,
    "status": NavSatStatus,
    "latitude": "float64",
    "longitude": "float64",
    "altitude": "float64",
    "position_covariance": Array("float64", 9),
    "position_covariance_type": "uint8",
}

PointCloud2: CoreSchema = {
    "__typename": "sensor_msgs/msg/PointCloud2",
    "header": Header,
    "height": "uint32",
    "width": "uint32",
    "fields": Sequence(PointField),
    "is_bigendian": "bool",
    "point_step": "uint32",
    "row_step": "uint32",
    "data": Sequence("uint8"),
    "is_dense": "bool",
}

CameraInfo: CoreSchema = {
    "__typename": "sensor_msgs/msg/CameraInfo",
    "header": Header,
    "height": "uint32",
    "width": "uint32",
    "distortion_model": "string",
    "d": Sequence("float64"),
    "k": Array("float64", 9),
    "r": Array("float64", 9),
    "p": Array("float64", 12),
    "binning_x": "uint32",
    "binning_y": "uint32",
    "roi": RegionOfInterest,
}

__all__ = [
    "BatteryState",
    "ChannelFloat32",
    "CompressedImage",
    "FluidPressure",
    "Illuminance",
    "Image",
    "Imu",
    "JointState",
    "Joy",
    "JoyFeedback",
    "LaserEcho",
    "LaserScan",
    "MagneticField",
    "MultiDOFJointState",
    "NavSatStatus",
    "PointField",
    "Range",
    "RegionOfInterest",
    "RelativeHumidity",
    "Temperature",
    "TimeReference",
    "PointCloud",
    "JoyFeedbackArray",
    "MultiEchoLaserScan",
    "NavSatFix",
    "PointCloud2",
    "CameraInfo",
]
