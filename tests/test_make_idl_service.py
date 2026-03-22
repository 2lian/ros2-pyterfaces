from typing import get_type_hints

import pytest

from ros2_pyterfaces import idl
from ros2_pyterfaces.all_srvs import (
    SetBool_Request,
    SetBool_Response,
    Trigger_Response,
)
from ros2_pyterfaces.service_msgs.msg import ServiceEventInfo


SETBOOL_HASH = (
    "RIHS01_abe9e4bb6b41b40e6789712c00ec8871923e089af3f667a79992a428cff2da0a"
)


def test_make_idl_service_builds_expected_service_and_event_types():
    generated_type = idl.make_idl_service(
        SetBool_Request,
        SetBool_Response,
        _module_name=__name__,
    )

    service_hints = get_type_hints(generated_type)
    event_type = service_hints["event_message"]
    event_hints = get_type_hints(event_type, include_extras=True)

    assert issubclass(generated_type, idl.IdlStruct)
    assert issubclass(generated_type, idl.IdlServiceStruct)
    assert idl.is_service_type(generated_type)
    assert generated_type.get_type_name() == "std_srvs/srv/SetBool"

    assert generated_type.Request is SetBool_Request
    assert generated_type.Response is SetBool_Response
    assert service_hints["request_message"] is SetBool_Request
    assert service_hints["response_message"] is SetBool_Response
    assert issubclass(event_type, idl.IdlStruct)
    assert issubclass(event_type, idl.IdlServiceEventStruct)
    assert event_type.get_type_name() == "std_srvs/srv/SetBool_Event"

    assert event_hints["info"] is ServiceEventInfo
    assert event_hints["request"] == idl.types.sequence[SetBool_Request, 1]
    assert event_hints["response"] == idl.types.sequence[SetBool_Response, 1]


def test_make_idl_service_rejects_mismatched_request_response_types():
    with pytest.raises(ValueError, match="must share the same service type name"):
        idl.make_idl_service(SetBool_Request, Trigger_Response, _module_name=__name__)
