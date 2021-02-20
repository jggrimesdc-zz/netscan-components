""" Project level settings """

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_PATH = Path(__file__).parent
RESOURCE_PATH = BASE_PATH.parent.parent / "resources"

KEYSPACES = ["mgmt", "dqm", "meta", "status", "analytics", "score"]

ACCOUNT_ID = os.getenv("ACCOUNT_ID", "dantenant")
USER_ID = os.getenv("USER_ID", "12345")
CLUSTER_ID = os.getenv("CLUSTER_ID", "7001")

QA_BASE_URL = "http://internal-ab964cfaba50c4b17b4b4865903c0aee-1757907119.us-east-2.elb.amazonaws.com:8080"
DEV_BASE_URL = "http://internal-ace8915737c3d457fb859c3b3061fa37-1961826497.us-east-2.elb.amazonaws.com:8080"

# Defaults to dev, but can be set to QA
ENVIRONMENT_MODE = os.getenv("ENVIRONMENT_MODE", "dev")

# BASE_URL is fetched from environment if set there, or from qa/dev base url
BASE_URL = os.getenv("BASE_URL")
if BASE_URL is None:
    if ENVIRONMENT_MODE == "dev":
        BASE_URL = DEV_BASE_URL
    elif ENVIRONMENT_MODE == "qa":
        BASE_URL = QA_BASE_URL

CLUSTER_ENDPOINT = "api/clusters/{CLUSTER_ID}"

REPLICATION_FACTOR_MAIN_DATACENTER = 3
REPLICATION_FACTOR_SECOND_DATACENTER = 1
