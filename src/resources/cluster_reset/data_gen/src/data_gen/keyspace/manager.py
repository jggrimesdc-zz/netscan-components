"""
Keyspace manager
"""
from data_gen.keyspace import Keyspace
from itertools import chain
from typing import List, Optional


class KeyspaceManager(object):
    __doc__ = __doc__

    def __init__(
            self, keyspaces: List[Keyspace], name: str, rules: Optional[List] = None
    ):
        self.name = name
        self.keyspaces = keyspaces
        self.rules = rules

    def get_column_set(self):
        columns = chain.from_iterable(keyspace.columns for keyspace in self.keyspaces)
        return set(columns)
