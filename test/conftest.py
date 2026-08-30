import pytest


@pytest.fixture
def expected_query_param():
    return lambda address, registers: "ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}".format(
        address >> 8,
        address & 255,
        registers >> 8,
        registers & 255,
    )
