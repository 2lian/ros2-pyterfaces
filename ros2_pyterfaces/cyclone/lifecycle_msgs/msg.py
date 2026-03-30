from dataclasses import dataclass, field
from typing import ClassVar, Literal

from ..idl import IdlStruct, types


@dataclass
class State(IdlStruct, typename="lifecycle_msgs/msg/State"):
    PRIMARY_STATE_UNKNOWN: ClassVar[Literal[0]] = 0
    PRIMARY_STATE_UNCONFIGURED: ClassVar[Literal[1]] = 1
    PRIMARY_STATE_INACTIVE: ClassVar[Literal[2]] = 2
    PRIMARY_STATE_ACTIVE: ClassVar[Literal[3]] = 3
    PRIMARY_STATE_FINALIZED: ClassVar[Literal[4]] = 4
    TRANSITION_STATE_CONFIGURING: ClassVar[Literal[10]] = 10
    TRANSITION_STATE_CLEANINGUP: ClassVar[Literal[11]] = 11
    TRANSITION_STATE_SHUTTINGDOWN: ClassVar[Literal[12]] = 12
    TRANSITION_STATE_ACTIVATING: ClassVar[Literal[13]] = 13
    TRANSITION_STATE_DEACTIVATING: ClassVar[Literal[14]] = 14
    TRANSITION_STATE_ERRORPROCESSING: ClassVar[Literal[15]] = 15

    id: types.uint8 = 0
    label: str = ""


@dataclass
class Transition(IdlStruct, typename="lifecycle_msgs/msg/Transition"):
    TRANSITION_CREATE: ClassVar[Literal[0]] = 0
    TRANSITION_CONFIGURE: ClassVar[Literal[1]] = 1
    TRANSITION_CLEANUP: ClassVar[Literal[2]] = 2
    TRANSITION_ACTIVATE: ClassVar[Literal[3]] = 3
    TRANSITION_DEACTIVATE: ClassVar[Literal[4]] = 4
    TRANSITION_UNCONFIGURED_SHUTDOWN: ClassVar[Literal[5]] = 5
    TRANSITION_INACTIVE_SHUTDOWN: ClassVar[Literal[6]] = 6
    TRANSITION_ACTIVE_SHUTDOWN: ClassVar[Literal[7]] = 7
    TRANSITION_DESTROY: ClassVar[Literal[8]] = 8
    TRANSITION_ON_CONFIGURE_SUCCESS: ClassVar[Literal[10]] = 10
    TRANSITION_ON_CONFIGURE_FAILURE: ClassVar[Literal[11]] = 11
    TRANSITION_ON_CONFIGURE_ERROR: ClassVar[Literal[12]] = 12
    TRANSITION_ON_CLEANUP_SUCCESS: ClassVar[Literal[20]] = 20
    TRANSITION_ON_CLEANUP_FAILURE: ClassVar[Literal[21]] = 21
    TRANSITION_ON_CLEANUP_ERROR: ClassVar[Literal[22]] = 22
    TRANSITION_ON_ACTIVATE_SUCCESS: ClassVar[Literal[30]] = 30
    TRANSITION_ON_ACTIVATE_FAILURE: ClassVar[Literal[31]] = 31
    TRANSITION_ON_ACTIVATE_ERROR: ClassVar[Literal[32]] = 32
    TRANSITION_ON_DEACTIVATE_SUCCESS: ClassVar[Literal[40]] = 40
    TRANSITION_ON_DEACTIVATE_FAILURE: ClassVar[Literal[41]] = 41
    TRANSITION_ON_DEACTIVATE_ERROR: ClassVar[Literal[42]] = 42
    TRANSITION_ON_SHUTDOWN_SUCCESS: ClassVar[Literal[50]] = 50
    TRANSITION_ON_SHUTDOWN_FAILURE: ClassVar[Literal[51]] = 51
    TRANSITION_ON_SHUTDOWN_ERROR: ClassVar[Literal[52]] = 52
    TRANSITION_ON_ERROR_SUCCESS: ClassVar[Literal[60]] = 60
    TRANSITION_ON_ERROR_FAILURE: ClassVar[Literal[61]] = 61
    TRANSITION_ON_ERROR_ERROR: ClassVar[Literal[62]] = 62
    TRANSITION_CALLBACK_SUCCESS: ClassVar[Literal[97]] = 97
    TRANSITION_CALLBACK_FAILURE: ClassVar[Literal[98]] = 98
    TRANSITION_CALLBACK_ERROR: ClassVar[Literal[99]] = 99

    id: types.uint8 = 0
    label: str = ""


@dataclass
class TransitionDescription(
    IdlStruct, typename="lifecycle_msgs/msg/TransitionDescription"
):
    transition: Transition = field(default_factory=Transition)
    start_state: State = field(default_factory=State)
    goal_state: State = field(default_factory=State)


@dataclass
class TransitionEvent(IdlStruct, typename="lifecycle_msgs/msg/TransitionEvent"):
    timestamp: types.uint64 = 0
    transition: Transition = field(default_factory=Transition)
    start_state: State = field(default_factory=State)
    goal_state: State = field(default_factory=State)
