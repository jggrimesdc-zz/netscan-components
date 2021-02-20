import boto3
import json
import pytest
from botocore.stub import Stubber
from pathlib import Path

ACCOUNT_ID = "dantenant"
USER_ID = "12345"
CLUSTER_ID = "1001"

headers = {
    'accept': '*/*',
    'X-netscan-CustomerAccountId': f'{ACCOUNT_ID}',
    'X-netscan-UserId': f'{USER_ID}',
    'Content-Type': 'application/json'
}

event_file_path = (
        Path(".") / "test" / "events_library.json"
)
with open(str(event_file_path), "r") as f:
    event_data = json.loads(f.read())["events"]

files_file_path = (
        Path(".") / "test" / "files_library.json"
)
with open(str(files_file_path), "r") as f:
    file_data = json.loads(f.read())["files"]

cyberscan_config_path = (
        Path(".") / "resources" / "cluster_reset" / "config"
)


@pytest.fixture
def context():
    return object()


@pytest.fixture
def events():
    return event_data


@pytest.fixture
def files():
    return file_data


@pytest.fixture(autouse=True)
def s3_stub():
    s3 = boto3.resource('s3')
    with Stubber(s3.meta.client) as stubber:
        yield stubber
        # stubber.assert_no_pending_responses()
