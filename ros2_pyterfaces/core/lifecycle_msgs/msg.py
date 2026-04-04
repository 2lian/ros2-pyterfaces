from .. import Array, BoundedString, CoreSchema, Sequence

State: CoreSchema = {
    "__typename": "lifecycle_msgs/msg/State",
    "id": "uint8",
    "label": "string",
}

Transition: CoreSchema = {
    "__typename": "lifecycle_msgs/msg/Transition",
    "id": "uint8",
    "label": "string",
}

TransitionDescription: CoreSchema = {
    "__typename": "lifecycle_msgs/msg/TransitionDescription",
    "transition": Transition,
    "start_state": State,
    "goal_state": State,
}

TransitionEvent: CoreSchema = {
    "__typename": "lifecycle_msgs/msg/TransitionEvent",
    "timestamp": "uint64",
    "transition": Transition,
    "start_state": State,
    "goal_state": State,
}

__all__ = [
    "State",
    "Transition",
    "TransitionDescription",
    "TransitionEvent",
]
