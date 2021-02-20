""" Project settings """
import os
from pathlib import Path

MAX_LIST_ITEMS = os.getenv("MAX_LIST_ITEMS", 10)
MIN_LIST_ITEMS = os.getenv("ALLOW_EMPTY_LISTS", 1)

MIN_DATETIME = os.getenv("MIN_DATETIME", "-10y")
MAX_DATETIME = os.getenv("MAX_DATETIME", "now")

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/tmp/new_data"))

HOST = os.getenv("HOST", "localhost")
CLUSTER_ID = os.getenv("CLUSTER_ID", -1)
API_KEY = os.getenv("API_KEY", "")

RULES_FILE = os.getenv('RULES_FILE', 'data/rules.json')
