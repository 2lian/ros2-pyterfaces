import pytest

from ros2_pyterfaces.cydr.idl import IdlStruct

from .utils import (
    CORE_MESSAGE_SCHEMAS_BY_TYPENAME,
    MESSAGE_TYPE_IDS,
    MESSAGE_TYPES,
)


@pytest.mark.parametrize("msg_type", MESSAGE_TYPES, ids=MESSAGE_TYPE_IDS)
def test_cydr_core_schema_matches_core_schema(msg_type: type[IdlStruct]) -> None:
    type_name = msg_type.get_type_name()
    assert type_name in CORE_MESSAGE_SCHEMAS_BY_TYPENAME

    assert msg_type.to_core_schema() == CORE_MESSAGE_SCHEMAS_BY_TYPENAME[type_name]
