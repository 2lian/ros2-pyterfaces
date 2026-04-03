from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..builtin_interfaces.msg import Duration
from ..geometry_msgs.msg import Point, Pose, Quaternion, Vector3
from ..sensor_msgs.msg import CompressedImage
from ..std_msgs.msg import ColorRGBA, Header

class ImageMarker(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/ImageMarker'
    __unsupported_reason__ = 'points is a collection of messages, which cydr does not support'
    pass

class InteractiveMarkerFeedback(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/InteractiveMarkerFeedback'
    header: Header = msgspec.field(default_factory=Header)
    client_id: types.string = b''
    marker_name: types.string = b''
    control_name: types.string = b''
    event_type: types.uint8 = np.uint8(0)
    pose: Pose = msgspec.field(default_factory=Pose)
    menu_entry_id: types.uint32 = np.uint32(0)
    mouse_point: Point = msgspec.field(default_factory=Point)
    mouse_point_valid: types.boolean = False

class InteractiveMarkerPose(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/InteractiveMarkerPose'
    header: Header = msgspec.field(default_factory=Header)
    pose: Pose = msgspec.field(default_factory=Pose)
    name: types.string = b''

class MenuEntry(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/MenuEntry'
    id: types.uint32 = np.uint32(0)
    parent_id: types.uint32 = np.uint32(0)
    title: types.string = b''
    command: types.string = b''
    command_type: types.uint8 = np.uint8(0)

class MeshFile(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/MeshFile'
    filename: types.string = b''
    data: types.NDArray[Any, types.UInt8] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint8))

class UVCoordinate(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/UVCoordinate'
    u: types.float32 = np.float32(0.0)
    v: types.float32 = np.float32(0.0)

class Marker(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/Marker'
    __unsupported_reason__ = 'points is a collection of messages, which cydr does not support'
    pass

class InteractiveMarkerControl(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/InteractiveMarkerControl'
    __unsupported_reason__ = 'markers is a collection of messages, which cydr does not support'
    pass

class MarkerArray(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/MarkerArray'
    __unsupported_reason__ = 'markers is a collection of messages, which cydr does not support'
    pass

class InteractiveMarker(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/InteractiveMarker'
    __unsupported_reason__ = 'menu_entries is a collection of messages, which cydr does not support'
    pass

class InteractiveMarkerInit(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/InteractiveMarkerInit'
    __unsupported_reason__ = 'markers is a collection of messages, which cydr does not support'
    pass

class InteractiveMarkerUpdate(JitStruct):
    __idl_typename__ = 'visualization_msgs/msg/InteractiveMarkerUpdate'
    __unsupported_reason__ = 'markers is a collection of messages, which cydr does not support'
    pass
