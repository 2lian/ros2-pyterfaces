# ROS 2 PyTerfaces IDL

ROS 2 message and service definitions, metadata, and serialization in Python.

Create new message types, (de)serialize them, compute the RIHS01 hash, and
convert to and from ROS 2 Python messages. ROS 2 `common_interfaces` are
reimplemented and tested to interoperate with ROS.

> [!NOTE]
> This is a low level tool to send/receive raw payload with ROS 2, and to set up communications on the RMW.

## Install

```bash
pip install git+https://github.com/2lian/ros2-pyterfaces.git
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
hash_rihs01 = Vector3.hash_rihs01()

# ROS 2 conversion
ros_msg_type = Vector3.to_ros_type()
ros_msg = my_msg.to_ros()
our_msg: Vector3 = Vector3.from_ros(ros_msg)
```

### Service

Services follow the ROS naming pattern: `*_Request`, `*_Response`, `*_Event`,
stored in small wrapper type. If you want less boilerplate, `make_idl_service(...)`
can generate the service wrapper and the `*_Event` type from a request and a
response type.

```python
from dataclasses import dataclass, field
from typing import ClassVar, Type

from ros2_pyterfaces import idl
from ros2_pyterfaces.service_msgs.msg import ServiceEventInfo

# Same classes definition as Messages for *_Request *_Response
@dataclass
class SetBool_Request(idl.IdlStruct, typename="std_srvs/srv/SetBool_Request"):
    data: bool = False


@dataclass
class SetBool_Response(idl.IdlStruct, typename="std_srvs/srv/SetBool_Response"):
    success: bool = False
    message: str = ""

# Helper function to create a service class from `*_Request` and `*_Response`
MySetBool = idl.make_idl_service(SetBool_Request, SetBool_Response)

# get the hash
ros_hash = MySetBool.hash_rihs01()

# instantiate the request or response objects, or even the service
some_request: SetBool_Request = MySetBool.Request(data=True)
some_response : SetBool_Response = MySetBool.Response(success=True, message="yey")
some_srv = MySetBool(SetBool_Request(data=True), SetBool_Response(success=True))

# Full manual definition, if needed for better static typing
@dataclass
class SetBool_Event(
    idl.IdlStruct,
    typename="std_srvs/srv/SetBool_Event",
):
    info: ServiceEventInfo = field(default_factory=ServiceEventInfo)
    request: idl.types.sequence[SetBool_Request, 1] = field(default_factory=list)
    response: idl.types.sequence[SetBool_Response, 1] = field(default_factory=list)


@dataclass
class SetBool(
    idl.IdlServiceStruct,
    typename="std_srvs/srv/SetBool",
):
    Request: ClassVar[Type[SetBool_Request]] = SetBool_Request
    Response: ClassVar[Type[SetBool_Response]] = SetBool_Response
    request_message: SetBool_Request = field(default_factory=SetBool_Request)
    response_message: SetBool_Response = field(default_factory=SetBool_Response)
    event_message: SetBool_Event = field(default_factory=SetBool_Event)
```

> [!WARNING]
> Not implemented yet:
> - Actions

## Included Packages

- `ros2_pyterfaces.builtin_interfaces`
- `ros2_pyterfaces.diagnostic_msgs`
- `ros2_pyterfaces.geometry_msgs`
- `ros2_pyterfaces.nav_msgs`
- `ros2_pyterfaces.sensor_msgs`
- `ros2_pyterfaces.service_msgs`
- `ros2_pyterfaces.shape_msgs`
- `ros2_pyterfaces.std_msgs`
- `ros2_pyterfaces.std_srvs`
- `ros2_pyterfaces.stereo_msgs`
- `ros2_pyterfaces.type_description_interfaces`
- `ros2_pyterfaces.trajectory_msgs`
- `ros2_pyterfaces.visualization_msgs`

## Structure

- `ros2_pyterfaces.idl`: IDL structure defining messages.
- `ros2_pyterfaces.<package>.msg`: Messages
- `ros2_pyterfaces.<package>.srv`: Services

> [!NOTE]
> Services are represented as `<Name>_Request`, `<Name>_Response`,
> `<Name>_Event`, and a small `<Name>` wrapper exposing
> `request_message`, `response_message`, and `event_message`.
