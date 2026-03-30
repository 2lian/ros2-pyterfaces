from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct

class State(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/State'
    id: types.uint8 = np.uint8(0)
    label: types.string = b''

class Transition(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/Transition'
    id: types.uint8 = np.uint8(0)
    label: types.string = b''

class TransitionDescription(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/TransitionDescription'
    transition: Transition = msgspec.field(default_factory=Transition)
    start_state: State = msgspec.field(default_factory=State)
    goal_state: State = msgspec.field(default_factory=State)

class TransitionEvent(JitStruct):
    __idl_typename__ = 'lifecycle_msgs/msg/TransitionEvent'
    timestamp: types.uint64 = np.uint64(0)
    transition: Transition = msgspec.field(default_factory=Transition)
    start_state: State = msgspec.field(default_factory=State)
    goal_state: State = msgspec.field(default_factory=State)
