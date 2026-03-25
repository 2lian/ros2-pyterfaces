from dataclasses import dataclass, field

from .. import idl
from .msg import State, Transition, TransitionDescription


@dataclass
class ChangeState_Request(idl.IdlStruct, typename="lifecycle_msgs/srv/ChangeState_Request"):
    transition: Transition = field(default_factory=Transition)


@dataclass
class ChangeState_Response(idl.IdlStruct, typename="lifecycle_msgs/srv/ChangeState_Response"):
    success: bool = False


ChangeState = idl.make_idl_service(ChangeState_Request, ChangeState_Response)
ChangeState_Event = ChangeState.Event


@dataclass
class GetAvailableStates_Request(
    idl.IdlStruct, typename="lifecycle_msgs/srv/GetAvailableStates_Request"
):
    pass


@dataclass
class GetAvailableStates_Response(
    idl.IdlStruct, typename="lifecycle_msgs/srv/GetAvailableStates_Response"
):
    available_states: idl.types.sequence[State] = field(default_factory=list)


GetAvailableStates = idl.make_idl_service(
    GetAvailableStates_Request, GetAvailableStates_Response
)
GetAvailableStates_Event = GetAvailableStates.Event


@dataclass
class GetAvailableTransitions_Request(
    idl.IdlStruct, typename="lifecycle_msgs/srv/GetAvailableTransitions_Request"
):
    pass


@dataclass
class GetAvailableTransitions_Response(
    idl.IdlStruct, typename="lifecycle_msgs/srv/GetAvailableTransitions_Response"
):
    available_transitions: idl.types.sequence[TransitionDescription] = field(
        default_factory=list
    )


GetAvailableTransitions = idl.make_idl_service(
    GetAvailableTransitions_Request, GetAvailableTransitions_Response
)
GetAvailableTransitions_Event = GetAvailableTransitions.Event


@dataclass
class GetState_Request(idl.IdlStruct, typename="lifecycle_msgs/srv/GetState_Request"):
    pass


@dataclass
class GetState_Response(idl.IdlStruct, typename="lifecycle_msgs/srv/GetState_Response"):
    current_state: State = field(default_factory=State)


GetState = idl.make_idl_service(GetState_Request, GetState_Response)
GetState_Event = GetState.Event
