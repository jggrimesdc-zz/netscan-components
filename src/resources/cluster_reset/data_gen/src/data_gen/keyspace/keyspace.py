from data_gen.keyspace import Column
from pathlib import Path
from typing import List


class Keyspace(object):
    """ Representation of a keyspace """

    def __init__(
            self, name: str, columns: List[str], primary_key: List[str], table_options: str
    ):
        self.name = name
        self.columns = [Column(column) for column in columns]
        self.primary_key = primary_key
        self.table_options = table_options

    def __contains__(self, other):
        return other in self.columns

    @property
    def filename(self):
        return f"{self.name}.ndjson"

    def reset_file(self, target_dir: Path):
        path = str(target_dir / self.filename)
        with open(path, "w"):
            pass

    def append_to_file(self, target_dir: Path, content: str):
        path = str(target_dir / self.filename)
        with open(path, "a+") as f:
            f.write(content)
            f.write("\n")
