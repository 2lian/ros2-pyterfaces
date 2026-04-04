from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Duration
from ..geometry_msgs.msg import Point, Pose, Quaternion, Vector3
from ..sensor_msgs.msg import CompressedImage
from ..std_msgs.msg import ColorRGBA, Header

ImageMarker: CoreSchema = {
    "__typename": "visualization_msgs/msg/ImageMarker",
    "header": Header,
    "ns": "string",
    "id": "int32",
    "type": "int32",
    "action": "int32",
    "position": Point,
    "scale": "float32",
    "outline_color": ColorRGBA,
    "filled": "uint8",
    "fill_color": ColorRGBA,
    "lifetime": Duration,
    "points": Sequence(Point),
    "outline_colors": Sequence(ColorRGBA),
}

InteractiveMarkerFeedback: CoreSchema = {
    "__typename": "visualization_msgs/msg/InteractiveMarkerFeedback",
    "header": Header,
    "client_id": "string",
    "marker_name": "string",
    "control_name": "string",
    "event_type": "uint8",
    "pose": Pose,
    "menu_entry_id": "uint32",
    "mouse_point": Point,
    "mouse_point_valid": "bool",
}

InteractiveMarkerPose: CoreSchema = {
    "__typename": "visualization_msgs/msg/InteractiveMarkerPose",
    "header": Header,
    "pose": Pose,
    "name": "string",
}

MenuEntry: CoreSchema = {
    "__typename": "visualization_msgs/msg/MenuEntry",
    "id": "uint32",
    "parent_id": "uint32",
    "title": "string",
    "command": "string",
    "command_type": "uint8",
}

MeshFile: CoreSchema = {
    "__typename": "visualization_msgs/msg/MeshFile",
    "filename": "string",
    "data": Sequence("uint8"),
}

UVCoordinate: CoreSchema = {
    "__typename": "visualization_msgs/msg/UVCoordinate",
    "u": "float32",
    "v": "float32",
}

Marker: CoreSchema = {
    "__typename": "visualization_msgs/msg/Marker",
    "header": Header,
    "ns": "string",
    "id": "int32",
    "type": "int32",
    "action": "int32",
    "pose": Pose,
    "scale": Vector3,
    "color": ColorRGBA,
    "lifetime": Duration,
    "frame_locked": "bool",
    "points": Sequence(Point),
    "colors": Sequence(ColorRGBA),
    "texture_resource": "string",
    "texture": CompressedImage,
    "uv_coordinates": Sequence(UVCoordinate),
    "text": "string",
    "mesh_resource": "string",
    "mesh_file": MeshFile,
    "mesh_use_embedded_materials": "bool",
}

InteractiveMarkerControl: CoreSchema = {
    "__typename": "visualization_msgs/msg/InteractiveMarkerControl",
    "name": "string",
    "orientation": Quaternion,
    "orientation_mode": "uint8",
    "interaction_mode": "uint8",
    "always_visible": "bool",
    "markers": Sequence(Marker),
    "independent_marker_orientation": "bool",
    "description": "string",
}

MarkerArray: CoreSchema = {
    "__typename": "visualization_msgs/msg/MarkerArray",
    "markers": Sequence(Marker),
}

InteractiveMarker: CoreSchema = {
    "__typename": "visualization_msgs/msg/InteractiveMarker",
    "header": Header,
    "pose": Pose,
    "name": "string",
    "description": "string",
    "scale": "float32",
    "menu_entries": Sequence(MenuEntry),
    "controls": Sequence(InteractiveMarkerControl),
}

InteractiveMarkerInit: CoreSchema = {
    "__typename": "visualization_msgs/msg/InteractiveMarkerInit",
    "server_id": "string",
    "seq_num": "uint64",
    "markers": Sequence(InteractiveMarker),
}

InteractiveMarkerUpdate: CoreSchema = {
    "__typename": "visualization_msgs/msg/InteractiveMarkerUpdate",
    "server_id": "string",
    "seq_num": "uint64",
    "type": "uint8",
    "markers": Sequence(InteractiveMarker),
    "poses": Sequence(InteractiveMarkerPose),
    "erases": Sequence("string"),
}

__all__ = [
    "ImageMarker",
    "InteractiveMarkerFeedback",
    "InteractiveMarkerPose",
    "MenuEntry",
    "MeshFile",
    "UVCoordinate",
    "Marker",
    "InteractiveMarkerControl",
    "MarkerArray",
    "InteractiveMarker",
    "InteractiveMarkerInit",
    "InteractiveMarkerUpdate",
]
