from dataclasses import dataclass, field

from ros2_pyterfaces.cyclone.idl import IdlStruct, types


@dataclass
class Time(IdlStruct, typename="builtin_interfaces/msg/Time"):
    sec: types.int32 = 0
    nanosec: types.uint32 = 0


@dataclass
class Header(IdlStruct, typename="std_msgs/msg/Header"):
    stamp: Time = field(default_factory=Time)
    frame_id: str = ""


@dataclass
class JointState(IdlStruct, typename="sensor_msgs/msg/JointState"):
    header: Header = field(default_factory=Header)
    name: types.sequence[str] = field(default_factory=list)
    position: types.sequence[types.float64] = field(default_factory=list)
    velocity: types.sequence[types.float64] = field(default_factory=list)
    effort: types.sequence[types.float64] = field(default_factory=list)


my_msg: JointState = JointState(
    header=Header(
        stamp=Time(sec=1, nanosec=2),
        frame_id="base_link",
    ),
    name=["joint_1", "joint_2"],
    position=[1.0, 2.0],
    velocity=[0.1, 0.2],
    effort=[0.0, 0.0],
)

# serialization
blob_bytes: bytes = my_msg.serialize()
my_msg_again: JointState = JointState.deserialize(blob_bytes)

# ROS 2 metadata
json_type_description = JointState.json_type_description()
ros_hash = JointState.hash_rihs01()

# ROS 2 conversion
ros_msg_type = JointState.to_ros_type()
ros_msg = my_msg.to_ros()
our_msg: JointState = JointState.from_ros(ros_msg)

