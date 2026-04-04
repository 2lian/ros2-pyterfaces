# ROS 2 PyTerfaces IDL



| Requirements | Compatibility | Tests |
|---|:---|:---:|
| [![python](https://img.shields.io/pypi/pyversions/ros2_pyterfaces?logo=python&logoColor=white&label=Python&color=%20blue)](https://pypi.org/project/ros2_pyterfaces/) <br>[![mit](https://img.shields.io/badge/License-MIT-gold)](https://opensource.org/license/mit) | [![ros](https://img.shields.io/badge/ROS_2-Kilted-blue?logo=ros)](https://github.com/ros2) <br> [![ros](https://img.shields.io/badge/ROS_2-Jazzy-blue?logo=ros)](https://github.com/ros2) <br> [![ros](https://img.shields.io/badge/ROS_2-Humble-blue?logo=ros)](https://github.com/ros2) <br> | `Humble`, `Jazzy`, `Kilted` <br> `ubuntu`, `windows`<br> [![Tests](https://github.com/2lian/ros2-pyterfaces/actions/workflows/test.yml/badge.svg)](https://github.com/2lian/ros2-pyterfaces/actions/workflows/test.yml) |

ROS 2 message and service definitions, metadata and serialization in Python.

Create new message types, (de)serialize them, compute the RIHS01 hash, and
convert to and from ROS 2 Python messages. All ROS 2 `common_interfaces` are
reimplemented, and every message tested to interoperate with ROS.

> [!NOTE]
> This is a low level tool to send/receive raw payload with ROS 2, and to set up communications on the RMW.

## Table of Contents

- [Install](#install)
- [Reliability](#reliability)
- [Example](#example)
  - [Message](#message)
  - [Service](#service)
  - [Utilities](#utilities)
- [Attribution](#attribution)
- [Replicated ROS 2 Repos](#replicated-ros-2-repos)
  - [Included Interfaces](#included-interfaces)

## Install

```bash
pip install ros2_pyterfaces[cyclone, cydr]
```

The library has three backends:

- `core`: normalized schema and message representation. This is plain Python, so you can easily do whatever you need. However, it cannot encode/decode.
- `cyclone`: This is the more complete IDL backend and the easiest one to hand-write. It is based on [Cyclone DDS Python](https://github.com/eclipse-cyclonedds/cyclonedds-python).
- `cydr`: This backend is much stricter about types and annotations, has some limitations, but is tremendously faster than Cyclone. It is based on [cydr](https://github.com/2lian/cydr).

Examples for the same `JointState` message in each style:

- Core: [`ros2_pyterfaces/examples/core_joint_state.py`](ros2_pyterfaces/examples/core_joint_state.py)
- Cyclone: [`ros2_pyterfaces/examples/cyclone_joint_state.py`](ros2_pyterfaces/examples/cyclone_joint_state.py)
- cydr: [`ros2_pyterfaces/examples/cydr_joint_state.py`](ros2_pyterfaces/examples/cydr_joint_state.py)

> [!NOTE]
> Some ROS distros have minor differences -- mainly `to_ros()` / `from_ros()`.
> To override the distro, either set the environment variable
> `ROS_DISTRO=YOUR_DISTRO` or set it in python 
> `ros2_pyterfaces.DISTRO = ros2_pyterfaces.Distro.YOUR_DISTRO` 
> (before importing other submodules).

## Reliability

Each message type in this library is heavily tested, for a total of more than
4000 tests, including randomized roundtrips through ROS 2. The goal
is 100% interoperability. Conversions, serialization, deserialization, hashes,
and raw payload exchange, are all exercised against ROS 2.

## Example

First, choose the layer that matches what you need. In this examples we use `cyclone`.

- `core` when you simply need a python dict.
- `cyclone` when you want a more ergonomic, all rounded dataclass.
- `cydr` when you want strict numpy types and higher performance.

### Message

```python
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
```

### Service

Services follow the ROS naming pattern: `*_Request`, `*_Response`, `*_Event`,
plus a small wrapper type. The serializable types are the request, response,
and service wrapper. With `cyclone`, the generated event type is also a usable
IDL struct. With `cydr`, the event type is just a placeholder because unsuported.
The top-level service type is usually created with `make_idl_service(...)`.
If you omit `event_type=...` (most cases), the factory generates the matching
service metadata for you.

```python
from dataclasses import dataclass
from ros2_pyterfaces.cyclone import idl

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

Messages can be converted to the normalized core representation (a json style
`dict` of `str`, `int`, `bytes`, and `list`) for comparisons, tests, snapshots,
and easier processing:

```python
core_schema = type(my_msg).to_core_schema()
core_msg = my_msg.to_core_message()

same_msg_again = type(my_msg).from_core_message(core_msg)
assert same_msg_again.to_core_message() == core_msg
```

The same core schema and core message can also be passed through
`ros2_pyterfaces.core` helpers when you want ROS conversion without depending on
a specific IDL backend.

## Attribution

### Dependencies By Backend

- `core`
  - [NumPy](https://numpy.org/)
  - ROS 2 Python message/service classes from the installed distro, when using ROS conversion helpers
- `cyclone`
  - [Cyclone DDS Python](https://github.com/eclipse-cyclonedds/cyclonedds-python) via `cyclonedds_idl`
- `cydr`
  - [cydr](https://github.com/2lian/cydr)
  - [msgspec](https://jcristharif.com/msgspec/)

### Replicated ROS 2 Messages Repos

- [`common_interfaces`](https://github.com/ros2/common_interfaces)
- [`rcl_interfaces`](https://github.com/ros2/rcl_interfaces)
- [`unique_identifier_msgs`](https://github.com/ros2/unique_identifier_msgs)

## Included Interfaces

- `ros2_pyterfaces.cyclone.builtin_interfaces`: [msg.py](ros2_pyterfaces/cyclone/builtin_interfaces/msg.py)
- `ros2_pyterfaces.cyclone.composition_interfaces`: [srv.py](ros2_pyterfaces/cyclone/composition_interfaces/srv.py)
- `ros2_pyterfaces.cyclone.diagnostic_msgs`: [msg.py](ros2_pyterfaces/cyclone/diagnostic_msgs/msg.py), [srv.py](ros2_pyterfaces/cyclone/diagnostic_msgs/srv.py)
- `ros2_pyterfaces.cyclone.geometry_msgs`: [msg.py](ros2_pyterfaces/cyclone/geometry_msgs/msg.py)
- `ros2_pyterfaces.cyclone.lifecycle_msgs`: [msg.py](ros2_pyterfaces/cyclone/lifecycle_msgs/msg.py), [srv.py](ros2_pyterfaces/cyclone/lifecycle_msgs/srv.py)
- `ros2_pyterfaces.cyclone.nav_msgs`: [msg.py](ros2_pyterfaces/cyclone/nav_msgs/msg.py), [srv.py](ros2_pyterfaces/cyclone/nav_msgs/srv.py)
- `ros2_pyterfaces.cyclone.rcl_interfaces`: [msg.py](ros2_pyterfaces/cyclone/rcl_interfaces/msg.py), [srv.py](ros2_pyterfaces/cyclone/rcl_interfaces/srv.py)
- `ros2_pyterfaces.cyclone.rosgraph_msgs`: [msg.py](ros2_pyterfaces/cyclone/rosgraph_msgs/msg.py)
- `ros2_pyterfaces.cyclone.sensor_msgs`: [msg.py](ros2_pyterfaces/cyclone/sensor_msgs/msg.py), [srv.py](ros2_pyterfaces/cyclone/sensor_msgs/srv.py)
- `ros2_pyterfaces.cyclone.service_msgs`: [msg.py](ros2_pyterfaces/cyclone/service_msgs/msg.py)
- `ros2_pyterfaces.cyclone.shape_msgs`: [msg.py](ros2_pyterfaces/cyclone/shape_msgs/msg.py)
- `ros2_pyterfaces.cyclone.statistics_msgs`: [msg.py](ros2_pyterfaces/cyclone/statistics_msgs/msg.py)
- `ros2_pyterfaces.cyclone.std_msgs`: [msg.py](ros2_pyterfaces/cyclone/std_msgs/msg.py)
- `ros2_pyterfaces.cyclone.std_srvs`: [srv.py](ros2_pyterfaces/cyclone/std_srvs/srv.py)
- `ros2_pyterfaces.cyclone.stereo_msgs`: [msg.py](ros2_pyterfaces/cyclone/stereo_msgs/msg.py)
- `ros2_pyterfaces.cyclone.test_msgs`: [msg.py](ros2_pyterfaces/cyclone/test_msgs/msg.py)
- `ros2_pyterfaces.cyclone.type_description_interfaces`: [msg.py](ros2_pyterfaces/cyclone/type_description_interfaces/msg.py), [srv.py](ros2_pyterfaces/cyclone/type_description_interfaces/srv.py)
- `ros2_pyterfaces.cyclone.trajectory_msgs`: [msg.py](ros2_pyterfaces/cyclone/trajectory_msgs/msg.py)
- `ros2_pyterfaces.cyclone.unique_identifier_msgs`: [msg.py](ros2_pyterfaces/cyclone/unique_identifier_msgs/msg.py)
- `ros2_pyterfaces.cyclone.visualization_msgs`: [msg.py](ros2_pyterfaces/cyclone/visualization_msgs/msg.py), [srv.py](ros2_pyterfaces/cyclone/visualization_msgs/srv.py)
