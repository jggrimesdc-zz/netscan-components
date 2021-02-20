import json
import requests
from data_gen import endpoints, settings
from data_gen.keyspace import KeyspaceManager
from pathlib import Path


def load_data(manager: KeyspaceManager, data_dir: Path):
    header = {
        "X-API-TOKEN": settings.API_KEY,
    }
    for keyspace in manager.keyspaces:
        with open(str(data_dir / keyspace.filename)) as f:
            url = endpoints.keyspace_table_insert(manager.name, keyspace.name)
            for row in f:
                data = json.loads(row.strip())
                requests.post(url, json=data, header=header)
    return True
