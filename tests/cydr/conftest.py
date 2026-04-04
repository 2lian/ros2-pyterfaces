import pytest

from ros2_pyterfaces.cydr import _compile_all


@pytest.fixture(scope="session", autouse=True)
def compile_cydr_types() -> None:
    _compile_all(max_workers=8)
