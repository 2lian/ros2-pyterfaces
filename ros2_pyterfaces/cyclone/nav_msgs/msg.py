from dataclasses import dataclass, field
from ..idl import IdlStruct, types
from ..geometry_msgs.msg import PoseStamped, Point, Pose, PoseWithCovariance, TwistWithCovariance, Accel, Twist, Wrench
from ..std_msgs.msg import Header
from ..builtin_interfaces.msg import Time

@dataclass
class Goals(IdlStruct, typename="nav_msgs/msg/Goals"):
    header: Header = field(default_factory=Header)
    goals: types.sequence[PoseStamped] = field(default_factory=list)


@dataclass
class GridCells(IdlStruct, typename="nav_msgs/msg/GridCells"):
    header: Header = field(default_factory=Header)
    cell_width: types.float32 = 0.0
    cell_height: types.float32 = 0.0
    cells: types.sequence[Point] = field(default_factory=list)


@dataclass
class MapMetaData(IdlStruct, typename="nav_msgs/msg/MapMetaData"):
    map_load_time: Time = field(default_factory=Time)
    resolution: types.float32 = 0.0
    width: types.uint32 = 0
    height: types.uint32 = 0
    origin: Pose = field(default_factory=Pose)


@dataclass
class Odometry(IdlStruct, typename="nav_msgs/msg/Odometry"):
    header: Header = field(default_factory=Header)
    child_frame_id: str = ""
    pose: PoseWithCovariance = field(default_factory=PoseWithCovariance)
    twist: TwistWithCovariance = field(default_factory=TwistWithCovariance)


@dataclass
class Path(IdlStruct, typename="nav_msgs/msg/Path"):
    header: Header = field(default_factory=Header)
    poses: types.sequence[PoseStamped] = field(default_factory=list)


@dataclass
class TrajectoryPoint(IdlStruct, typename="nav_msgs/msg/TrajectoryPoint"):
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)
    velocity: Twist = field(default_factory=Twist)
    acceleration: Accel = field(default_factory=Accel)
    effort: Wrench = field(default_factory=Wrench)


@dataclass
class OccupancyGrid(IdlStruct, typename="nav_msgs/msg/OccupancyGrid"):
    header: Header = field(default_factory=Header)
    info: MapMetaData = field(default_factory=MapMetaData)
    data: types.sequence[types.int8] = field(default_factory=list)


@dataclass
class Trajectory(IdlStruct, typename="nav_msgs/msg/Trajectory"):
    header: Header = field(default_factory=Header)
    points: types.sequence[TrajectoryPoint] = field(default_factory=list)
