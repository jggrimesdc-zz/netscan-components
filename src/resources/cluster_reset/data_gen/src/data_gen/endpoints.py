"""
API endpoints
"""
from data_gen.settings import HOST, CLUSTER_ID


def keyspace_table_insert(keyspace: str, table: str) -> str:
    return f"https://{HOST}/api/clusters/{CLUSTER_ID}/keyspaces/{keyspace}/tables/{table}/insert"
