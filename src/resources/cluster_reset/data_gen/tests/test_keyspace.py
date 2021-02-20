import pytest
from data_gen.keyspace import Column, Keyspace, KeyspaceManager, KeyspaceReader
from pathlib import Path


def test_column():
    col_definition = "foo text"
    col = Column(col_definition)

    assert col.name == "foo"
    assert col.type == "text"
    assert col.definition == col_definition
    assert str(col)
    assert repr(col)
    assert col != col_definition

    with pytest.raises(TypeError):
        Column('asdf')


def test_column_hashable():
    a = Column("foo bar")
    b = Column("foo bar")
    assert a == b
    assert hash(a) == hash(b)


def test_keyspace():
    cols = ["asdf text", "foo int", "bar timestamp"]
    col = Column(cols[0])
    primary_key = ["foo asdf"]
    keyspace = Keyspace("foo", cols, primary_key, "order by asdf")

    assert col in keyspace
    assert keyspace.filename

    path = Path("tmp/test/test_keyspace")
    path.mkdir(parents=True, exist_ok=True)

    keyspace.reset_file(path)

    with open(str(path / keyspace.filename)) as f:
        assert len(f.read()) == 0

    keyspace.append_to_file(path, "asdf")

    with open(str(path / keyspace.filename)) as f:
        assert len(f.read()) > 0


def test_keyspace_reader():
    path = Path("data/scan/status")

    reader = KeyspaceReader(str(path), "**/*.json")
    manager = reader.read()

    assert len(manager.keyspaces) > 0
    assert all(len(keyspace.columns) for keyspace in manager.keyspaces)


def test_keyspace_manager(manager):
    assert manager.get_column_set()
