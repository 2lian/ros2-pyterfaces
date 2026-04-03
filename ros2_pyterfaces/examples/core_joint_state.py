from ros2_pyterfaces import core

Time: core.CoreSchema = {
    "__typename": "builtin_interfaces/msg/Time",
    "sec": "int32",
    "nanosec": "uint32",
}

Header: core.CoreSchema = {
    "__typename": "std_msgs/msg/Header",
    "stamp": Time,
    "frame_id": "string",
}

JointState: core.CoreSchema = {
    "__typename": "sensor_msgs/msg/JointState",
    "header": Header,
    "name": core.Sequence("string"),
    "position": core.Sequence("float64"),
    "velocity": core.Sequence("float64"),
    "effort": core.Sequence("float64"),
}

my_msg: dict[str, object] = {
    "__typename": JointState["__typename"],
    "header": {
        "__typename": "std_msgs/msg/Header",
        "stamp": {
            "__typename": "builtin_interfaces/msg/Time",
            "sec": 1,
            "nanosec": 2,
        },
        "frame_id": "base_link",
    },
    "name": ["joint_1", "joint_2"],
    "position": [1.0, 2.0],
    "velocity": [0.1, 0.2],
    "effort": [0.0, 0.0],
}

# verification
core.verify_message(JointState, my_msg)

# ROS 2 metadata
json_type_description = core.json_type_description(JointState)
ros_hash = core.hash_rihs01(JointState)

# ROS 2 conversion
ros_msg_type = core.to_ros_type(JointState)
ros_msg = core.to_ros(my_msg)
our_msg: dict[str, object] = core.from_ros(JointState, ros_msg)

