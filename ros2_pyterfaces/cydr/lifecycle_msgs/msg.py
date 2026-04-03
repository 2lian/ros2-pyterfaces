from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct

class State(IdlStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/State'
    id: types.uint8 = np.uint8(0)
    label: types.string = b''

class Transition(IdlStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/Transition'
    id: types.uint8 = np.uint8(0)
    label: types.string = b''

class TransitionDescription(IdlStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/TransitionDescription'
    transition: Transition = msgspec.field(default_factory=Transition)
    start_state: State = msgspec.field(default_factory=State)
    goal_state: State = msgspec.field(default_factory=State)

class TransitionEvent(IdlStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/TransitionEvent'
    timestamp: types.uint64 = np.uint64(0)
    transition: Transition = msgspec.field(default_factory=Transition)
    start_state: State = msgspec.field(default_factory=State)
    goal_state: State = msgspec.field(default_factory=State)
