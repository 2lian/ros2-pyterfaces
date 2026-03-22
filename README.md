# ROS 2 PyTerfaces IDL

ROS 2 message creation, common interfaces and metadata. Written in python.

Create new message types, (de)serialize messages, compute the rihs01 hash,
interoperate with ROS 2 and more. ROS 2 `common_interfaces` fully reimplemented and
tested to communicate to/from ROS.

> [!NOTE]
> This is a low level tool to send/receive raw payload with ROS 2, and to set up communications on the RMW.

## Example

```python
from ros2_pyterfaces.idl import IdlStruct, types

@dataclass
class Vector3(IdlStruct, typename="geometry_msgs/msg/Vector3"):
    x: types.float64 = 0.0
    y: types.float64 = 0.0
    z: types.float64 = 0.0

my_msg: Vector3 = Vector3(1,2,3)

# serialization
blob_bytes: bytes = Vector3.serialize()
my_msg_again: Vector3 = Vector3.deserialize(blob_bytes)

# ROS 2 metadata
json_type_description = Vector3.json_type_description()
hash_rihs01 = Vector3.hash_rihs01()

# ROS 2 mutation
ros_msg_type = Vector3.to_ros_type()
ros_msg = Vector3(1,2,3).to_ros()
our_msg: Vector3 = Vector3.from_ros(ros_msg)
```

> [!WARNING]
> Not implemented yet:
> - Actions

## All ROS 2 `common_interfaces` Included:

- `ros2_pyterfaces.builtin_interfaces`
- `ros2_pyterfaces.diagnostic_msgs`
- `ros2_pyterfaces.geometry_msgs`
- `ros2_pyterfaces.nav_msgs`
- `ros2_pyterfaces.sensor_msgs`
- `ros2_pyterfaces.shape_msgs`
- `ros2_pyterfaces.std_msgs`
- `ros2_pyterfaces.std_srvs`
- `ros2_pyterfaces.stereo_msgs`
- `ros2_pyterfaces.trajectory_msgs`
- `ros2_pyterfaces.visualization_msgs`

## Structure

- `ros2_pyterfaces.idl`: IDL structure defining messages.
- `ros2_pyterfaces.<package>.msg`: Messages
- `ros2_pyterfaces.<package>.srv`: Services

> [!NOTE]
> Services are represented as `<Name>_Request`, `<Name>_Response`, and a small `<Name>` wrapper exposing `Request` and `Response`.
