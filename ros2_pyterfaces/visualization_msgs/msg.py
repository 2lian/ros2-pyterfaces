from dataclasses import dataclass, field
from typing import Literal

from ..builtin_interfaces.msg import Duration
from ..geometry_msgs.msg import Point, Pose, Quaternion, Vector3
from ..idl import IdlStruct, types
from ..sensor_msgs.msg import CompressedImage
from ..std_msgs.msg import ColorRGBA, Header


@dataclass
class ImageMarker(IdlStruct, typename="visualization_msgs/msg/ImageMarker"):
    CIRCLE: Literal[0] = 0
    LINE_STRIP: Literal[1] = 1
    LINE_LIST: Literal[2] = 2
    POLYGON: Literal[3] = 3
    POINTS: Literal[4] = 4
    ADD: Literal[0] = 0
    REMOVE: Literal[1] = 1
    header: Header = field(default_factory=Header)
    ns: str = ""
    id: types.int32 = 0
    type: types.int32 = 0
    action: types.int32 = 0
    position: Point = field(default_factory=Point)
    scale: types.float32 = 0.0
    outline_color: ColorRGBA = field(default_factory=ColorRGBA)
    filled: types.uint8 = 0
    fill_color: ColorRGBA = field(default_factory=ColorRGBA)
    lifetime: Duration = field(default_factory=Duration)
    points: types.sequence[Point] = field(default_factory=list)
    outline_colors: types.sequence[ColorRGBA] = field(default_factory=list)


@dataclass
class InteractiveMarkerFeedback(
    IdlStruct, typename="visualization_msgs/msg/InteractiveMarkerFeedback"
):
    KEEP_ALIVE: Literal[0] = 0
    POSE_UPDATE: Literal[1] = 1
    MENU_SELECT: Literal[2] = 2
    BUTTON_CLICK: Literal[3] = 3
    MOUSE_DOWN: Literal[4] = 4
    MOUSE_UP: Literal[5] = 5
    header: Header = field(default_factory=Header)
    client_id: str = ""
    marker_name: str = ""
    control_name: str = ""
    event_type: types.uint8 = 0
    pose: Pose = field(default_factory=Pose)
    menu_entry_id: types.uint32 = 0
    mouse_point: Point = field(default_factory=Point)
    mouse_point_valid: bool = False


@dataclass
class InteractiveMarkerPose(
    IdlStruct, typename="visualization_msgs/msg/InteractiveMarkerPose"
):
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)
    name: str = ""


@dataclass
class MenuEntry(IdlStruct, typename="visualization_msgs/msg/MenuEntry"):
    FEEDBACK: Literal[0] = 0
    ROSRUN: Literal[1] = 1
    ROSLAUNCH: Literal[2] = 2
    id: types.uint32 = 0
    parent_id: types.uint32 = 0
    title: str = ""
    command: str = ""
    command_type: types.uint8 = 0


@dataclass
class MeshFile(IdlStruct, typename="visualization_msgs/msg/MeshFile"):
    filename: str = ""
    data: types.sequence[types.uint8] = field(default_factory=list)


@dataclass
class UVCoordinate(IdlStruct, typename="visualization_msgs/msg/UVCoordinate"):
    u: types.float32 = 0.0
    v: types.float32 = 0.0


@dataclass
class Marker(IdlStruct, typename="visualization_msgs/msg/Marker"):
    ARROW: Literal[0] = 0
    CUBE: Literal[1] = 1
    SPHERE: Literal[2] = 2
    CYLINDER: Literal[3] = 3
    LINE_STRIP: Literal[4] = 4
    LINE_LIST: Literal[5] = 5
    CUBE_LIST: Literal[6] = 6
    SPHERE_LIST: Literal[7] = 7
    POINTS: Literal[8] = 8
    TEXT_VIEW_FACING: Literal[9] = 9
    MESH_RESOURCE: Literal[10] = 10
    TRIANGLE_LIST: Literal[11] = 11
    ARROW_STRIP: Literal[12] = 12
    ADD: Literal[0] = 0
    MODIFY: Literal[0] = 0
    DELETE: Literal[2] = 2
    DELETEALL: Literal[3] = 3
    header: Header = field(default_factory=Header)
    ns: str = ""
    id: types.int32 = 0
    type: types.int32 = 0
    action: types.int32 = 0
    pose: Pose = field(default_factory=Pose)
    scale: Vector3 = field(default_factory=Vector3)
    color: ColorRGBA = field(default_factory=ColorRGBA)
    lifetime: Duration = field(default_factory=Duration)
    frame_locked: bool = False
    points: types.sequence[Point] = field(default_factory=list)
    colors: types.sequence[ColorRGBA] = field(default_factory=list)
    texture_resource: str = ""
    texture: CompressedImage = field(default_factory=CompressedImage)
    uv_coordinates: types.sequence[UVCoordinate] = field(default_factory=list)
    text: str = ""
    mesh_resource: str = ""
    mesh_file: MeshFile = field(default_factory=MeshFile)
    mesh_use_embedded_materials: bool = False


@dataclass
class InteractiveMarkerControl(
    IdlStruct, typename="visualization_msgs/msg/InteractiveMarkerControl"
):
    INHERIT: Literal[0] = 0
    FIXED: Literal[1] = 1
    VIEW_FACING: Literal[2] = 2
    NONE: Literal[0] = 0
    MENU: Literal[1] = 1
    BUTTON: Literal[2] = 2
    MOVE_AXIS: Literal[3] = 3
    MOVE_PLANE: Literal[4] = 4
    ROTATE_AXIS: Literal[5] = 5
    MOVE_ROTATE: Literal[6] = 6
    MOVE_3D: Literal[7] = 7
    ROTATE_3D: Literal[8] = 8
    MOVE_ROTATE_3D: Literal[9] = 9
    name: str = ""
    orientation: Quaternion = field(default_factory=Quaternion)
    orientation_mode: types.uint8 = 0
    interaction_mode: types.uint8 = 0
    always_visible: bool = False
    markers: types.sequence[Marker] = field(default_factory=list)
    independent_marker_orientation: bool = False
    description: str = ""


@dataclass
class MarkerArray(IdlStruct, typename="visualization_msgs/msg/MarkerArray"):
    markers: types.sequence[Marker] = field(default_factory=list)


@dataclass
class InteractiveMarker(IdlStruct, typename="visualization_msgs/msg/InteractiveMarker"):
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)
    name: str = ""
    description: str = ""
    scale: types.float32 = 0.0
    menu_entries: types.sequence[MenuEntry] = field(default_factory=list)
    controls: types.sequence[InteractiveMarkerControl] = field(default_factory=list)


@dataclass
class InteractiveMarkerInit(
    IdlStruct, typename="visualization_msgs/msg/InteractiveMarkerInit"
):
    server_id: str = ""
    seq_num: types.uint64 = 0
    markers: types.sequence[InteractiveMarker] = field(default_factory=list)


@dataclass
class InteractiveMarkerUpdate(
    IdlStruct, typename="visualization_msgs/msg/InteractiveMarkerUpdate"
):
    KEEP_ALIVE: Literal[0] = 0
    UPDATE: Literal[1] = 1
    server_id: str = ""
    seq_num: types.uint64 = 0
    type: types.uint8 = 0
    markers: types.sequence[InteractiveMarker] = field(default_factory=list)
    poses: types.sequence[InteractiveMarkerPose] = field(default_factory=list)
    erases: types.sequence[str] = field(default_factory=list)
