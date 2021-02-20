import json
from data_gen.generate.fake_column import fake_column_data
from data_gen.keyspace import Column, KeyspaceManager
from pathlib import Path
from shutil import rmtree
from typing import Set, Optional


def fake_data(
        manager: KeyspaceManager,
        output_dir: Path,
        n_rows: int = 5,
        override_file: Optional[Path] = None,
):
    if output_dir.exists():
        rmtree(str(output_dir))
    output_dir.mkdir(exist_ok=True, parents=True)

    for keyspace in manager.keyspaces:
        keyspace.reset_file(output_dir)

    if override_file:
        with open(str(override_file)) as f:
            override_data = [json.loads(x.strip()) for x in f]

    for row_num in range(n_rows):
        row_data = make_row_data(manager)
        if override_file:
            row_data.update(override_data[row_num])
        for keyspace in manager.keyspaces:
            keyspace_row = {
                column.name: row_data.get(column.name) for column in keyspace.columns
            }
            keyspace.append_to_file(output_dir, json.dumps(keyspace_row))


def make_row_data(manager: KeyspaceManager) -> dict:
    return {column.name: fake_column_data(column, extra_rules=manager.rules) for column in manager.get_column_set()}
