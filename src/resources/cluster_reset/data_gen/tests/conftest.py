import pytest

from data_gen.keyspace import KeyspaceReader, KeyspaceManager


@pytest.fixture(params=["data/scan/analytics", "data/scan/status"])
def manager(request) -> KeyspaceManager:
    reader = KeyspaceReader(request.param)
    return reader.read()
