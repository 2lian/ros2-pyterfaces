# ROS 2 PyTerfaces IDL

ROS 2 message and service definitions, metadata and serialization in Python.

Create new message types, (de)serialize them, compute the RIHS01 hash, and
convert to and from ROS 2 Python messages. All ROS 2 `common_interfaces` are
reimplemented, and every message tested to interoperate with ROS.

Based on [Cyclone DDS IDL](https://cyclonedds.io/docs/cyclonedds-python/latest/idl.html), but specialized for ROS 2.

> [!NOTE]
> This is a low level tool to send/receive raw payload with ROS 2, and to set up communications on the RMW.

## Table of Contents

- [Install](#install)
- [Example](#example)
  - [Message](#message)
  - [Service](#service)
  - [Utilities](#utilities)
- [Attribution](#attribution)
- [Replicated ROS 2 Repos](#replicated-ros-2-repos)
  - [Included Interfaces](#included-interfaces)

## Install

```bash
pip install ros2_pyterfaces
```

## Example

### Message

```python
from dataclasses import dataclass
from ros2_pyterfaces.idl import IdlStruct, types

@dataclass
class Vector3(IdlStruct, typename="geometry_msgs/msg/Vector3"):
    x: types.float64 = 0.0
    y: types.float64 = 0.0
    z: types.float64 = 0.0

my_msg: Vector3 = Vector3(1,2,3)

# serialization
blob_bytes: bytes = my_msg.serialize()
my_msg_again: Vector3 = Vector3.deserialize(blob_bytes)

# ROS 2 metadata
json_type_description = Vector3.json_type_description()
ros_hash = Vector3.hash_rihs01()

# ROS 2 conversion
ros_msg_type = Vector3.to_ros_type()
ros_msg = my_msg.to_ros()
our_msg: Vector3 = Vector3.from_ros(ros_msg)
```

### Service

Services follow the ROS naming pattern: `*_Request`, `*_Response`, `*_Event`,
plus a small wrapper type. The serializable types are the request, response,
and event dataclasses. The top-level service type is usually created with
`make_idl_service(...)`. If you omit `event_type=...` (most cases), the factory
generates a matching event type for you.

```python
from dataclasses import dataclass
from ros2_pyterfaces import idl

# Same classes definition as Messages for *_Request *_Response
@dataclass
class SetBool_Request(idl.IdlStruct, typename="std_srvs/srv/SetBool_Request"):
    data: bool = False


@dataclass
class SetBool_Response(idl.IdlStruct, typename="std_srvs/srv/SetBool_Response"):
    success: bool = False
    message: str = ""

# Top-level service type
SetBool = idl.make_idl_service(SetBool_Request, SetBool_Response)

# Serialization
some_request: SetBool_Request = SetBool.Request(data=True)
some_response: SetBool_Response = SetBool.Response(success=True, message="yey")

# ROS 2 metadata
json_type_description = SetBool.json_type_description()
ros_hash = SetBool.hash_rihs01()

# ROS 2 conversion
ros_srv_type = SetBool.to_ros_type()

ros_request = some_request.to_ros()
request_again = SetBool.Request.from_ros(ros_request)

ros_response = some_response.to_ros()
response_again = SetBool.Response.from_ros(ros_response)
```

> [!WARNING]
> Not implemented yet:
> - Actions

### Utilities

You can normalize messages to plain nested Python data for comparisons, tests,
and snapshots:

```python
from ros2_pyterfaces import idl

plain = idl.message_to_plain_data(my_msg)
plain_ros = idl.message_to_plain_data(my_msg.to_ros(), type(my_msg))
assert plain == plain_ros
```

There is also a deterministic random message generator for repeatable tests:

```python
from ros2_pyterfaces.geometry_msgs.msg import Vector3
from ros2_pyterfaces.utils.random import random_message

msg = random_message(Vector3)
same_msg_again = random_message(Vector3)
assert msg == same_msg_again
```

## Attribution

The low-level IDL model, serialization behavior, and part of the user API are
dependent on (fantastic) Cyclone DDS Python's idl: https://github.com/eclipse-cyclonedds/cyclonedds-python.

### Replicated ROS 2  Messages Repos

- [`common_interfaces`](https://github.com/ros2/common_interfaces)
- [`rcl_interfaces`](https://github.com/ros2/rcl_interfaces)
- [`unique_identifier_msgs`](https://github.com/ros2/unique_identifier_msgs)

## Included Interfaces

- `ros2_pyterfaces.builtin_interfaces`: [msg.py](ros2_pyterfaces/builtin_interfaces/msg.py)
- `ros2_pyterfaces.composition_interfaces`: [srv.py](ros2_pyterfaces/composition_interfaces/srv.py)
- `ros2_pyterfaces.diagnostic_msgs`: [msg.py](ros2_pyterfaces/diagnostic_msgs/msg.py), [srv.py](ros2_pyterfaces/diagnostic_msgs/srv.py)
- `ros2_pyterfaces.geometry_msgs`: [msg.py](ros2_pyterfaces/geometry_msgs/msg.py)
- `ros2_pyterfaces.lifecycle_msgs`: [msg.py](ros2_pyterfaces/lifecycle_msgs/msg.py), [srv.py](ros2_pyterfaces/lifecycle_msgs/srv.py)
- `ros2_pyterfaces.nav_msgs`: [msg.py](ros2_pyterfaces/nav_msgs/msg.py), [srv.py](ros2_pyterfaces/nav_msgs/srv.py)
- `ros2_pyterfaces.rcl_interfaces`: [msg.py](ros2_pyterfaces/rcl_interfaces/msg.py), [srv.py](ros2_pyterfaces/rcl_interfaces/srv.py)
- `ros2_pyterfaces.rosgraph_msgs`: [msg.py](ros2_pyterfaces/rosgraph_msgs/msg.py)
- `ros2_pyterfaces.sensor_msgs`: [msg.py](ros2_pyterfaces/sensor_msgs/msg.py), [srv.py](ros2_pyterfaces/sensor_msgs/srv.py)
- `ros2_pyterfaces.service_msgs`: [msg.py](ros2_pyterfaces/service_msgs/msg.py)
- `ros2_pyterfaces.shape_msgs`: [msg.py](ros2_pyterfaces/shape_msgs/msg.py)
- `ros2_pyterfaces.statistics_msgs`: [msg.py](ros2_pyterfaces/statistics_msgs/msg.py)
- `ros2_pyterfaces.std_msgs`: [msg.py](ros2_pyterfaces/std_msgs/msg.py)
- `ros2_pyterfaces.std_srvs`: [srv.py](ros2_pyterfaces/std_srvs/srv.py)
- `ros2_pyterfaces.stereo_msgs`: [msg.py](ros2_pyterfaces/stereo_msgs/msg.py)
- `ros2_pyterfaces.test_msgs`: [msg.py](ros2_pyterfaces/test_msgs/msg.py)
- `ros2_pyterfaces.type_description_interfaces`: [msg.py](ros2_pyterfaces/type_description_interfaces/msg.py), [srv.py](ros2_pyterfaces/type_description_interfaces/srv.py)
- `ros2_pyterfaces.trajectory_msgs`: [msg.py](ros2_pyterfaces/trajectory_msgs/msg.py)
- `ros2_pyterfaces.unique_identifier_msgs`: [msg.py](ros2_pyterfaces/unique_identifier_msgs/msg.py)
- `ros2_pyterfaces.visualization_msgs`: [msg.py](ros2_pyterfaces/visualization_msgs/msg.py), [srv.py](ros2_pyterfaces/visualization_msgs/srv.py)
