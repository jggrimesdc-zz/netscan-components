""" Reads in all keyspaces from a folder """

import json
import os
from data_gen import settings, exceptions
from data_gen.keyspace import Keyspace, KeyspaceManager
from pathlib import Path
from typing import Optional


class KeyspaceReader(object):
    __doc__ = __doc__

    def __init__(
            self,
            path: str,
            glob_pattern: str = "**/*.json",
            rules_file: Optional[str] = "rules.json",
            keyspace_name: Optional[str] = None,
    ):
        self.path = Path(path)
        self.glob_pattern = glob_pattern
        self.rules_file = rules_file
        self.keyspace_name = keyspace_name or self.path.parts[-1]

    def read(self):
        from data_gen.generate import Rule

        keyspaces = []
        rules = None

        file_paths = [x for x in self.path.glob(self.glob_pattern)]
        if not file_paths:
            raise exceptions.NoTablesInKeyspace(
                f'No table definitions were found in keyspace "{self.path}" with glob pattern "{self.glob_pattern}".'
            )

        for file_path in file_paths:
            with open(str(file_path), "r") as f:
                data = json.loads(f.read())
            if self.rules_file and file_path.match(self.rules_file):
                rules = Rule.get_list_from_file(str(file_path))
                continue
            keyspaces.append(
                Keyspace(
                    name=data["name"],
                    columns=data["columnDefinitions"],
                    primary_key=data["primaryKey"],
                    table_options=data["tableOptions"],
                )
            )

        return KeyspaceManager(keyspaces, name=self.keyspace_name, rules=rules)
