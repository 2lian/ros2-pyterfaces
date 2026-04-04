from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..lifecycle_msgs.msg import State, Transition, TransitionDescription

ChangeState_Request: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/ChangeState_Request",
    "transition": Transition,
}

ChangeState_Response: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/ChangeState_Response",
    "success": "bool",
}

GetAvailableStates_Request: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/GetAvailableStates_Request",
}

GetAvailableStates_Response: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/GetAvailableStates_Response",
    "available_states": Sequence(State),
}

GetAvailableTransitions_Request: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/GetAvailableTransitions_Request",
}

GetAvailableTransitions_Response: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/GetAvailableTransitions_Response",
    "available_transitions": Sequence(TransitionDescription),
}

GetState_Request: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/GetState_Request",
}

GetState_Response: CoreSchema = {
    "__typename": "lifecycle_msgs/srv/GetState_Response",
    "current_state": State,
}

ChangeState: CoreSchema = make_srv_schema(ChangeState_Request, ChangeState_Response, typename="lifecycle_msgs/srv/ChangeState")
ChangeState_Event: CoreSchema = ChangeState["event_message"]

GetAvailableStates: CoreSchema = make_srv_schema(GetAvailableStates_Request, GetAvailableStates_Response, typename="lifecycle_msgs/srv/GetAvailableStates")
GetAvailableStates_Event: CoreSchema = GetAvailableStates["event_message"]

GetAvailableTransitions: CoreSchema = make_srv_schema(GetAvailableTransitions_Request, GetAvailableTransitions_Response, typename="lifecycle_msgs/srv/GetAvailableTransitions")
GetAvailableTransitions_Event: CoreSchema = GetAvailableTransitions["event_message"]

GetState: CoreSchema = make_srv_schema(GetState_Request, GetState_Response, typename="lifecycle_msgs/srv/GetState")
GetState_Event: CoreSchema = GetState["event_message"]

__all__ = [
    "ChangeState_Request",
    "ChangeState_Response",
    "GetAvailableStates_Request",
    "GetAvailableStates_Response",
    "GetAvailableTransitions_Request",
    "GetAvailableTransitions_Response",
    "GetState_Request",
    "GetState_Response",
    "ChangeState_Event",
    "ChangeState",
    "GetAvailableStates_Event",
    "GetAvailableStates",
    "GetAvailableTransitions_Event",
    "GetAvailableTransitions",
    "GetState_Event",
    "GetState",
]
