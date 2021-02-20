from __future__ import print_function

import datetime
import json
import os
import re
import requests
from scan_api_lib import RequestUtils
from scan_api_lib import WCaaSUtils

service_tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID")
cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID")
crud_api_url = os.environ.get("CRUD_API_URL")
meta_data_keyspace_id = os.environ.get("META_DATA_KEYSPACE")
mgmt_keyspace_id = os.environ.get("MGMT_KEYSPACE")


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))

    # VALIDATE INPUT #
    headers = event["headers"]

    invalid_fields = {}

    if "x-netscan-customeraccountid" not in headers:
        invalid_fields["x-netscan-customeraccountid"] = "Not Present"
    if "x-netscan-userid" not in headers:
        invalid_fields["x-netscan-userid"] = "Not Present"

    if len(invalid_fields.keys()) > 0:
        response_body = {
            "errorMessage": "Malformed Request",
            "errorDetails": invalid_fields
        }
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {},
            "multiValueHeaders": {},
            "body": json.dumps(response_body)
        }

    if event["pathParameters"]:
        schedule_id = event["pathParameters"].get("schedule_id", None)

    netscan_customer_account_id = str(headers["x-netscan-customeraccountid"]).strip()
    netscan_user_id = str(headers["x-netscan-userid"]).strip()
    user_id_matcher = re.compile("^[a-zA-Z0-9_]+$")

    if not user_id_matcher.match(netscan_customer_account_id):
        invalid_fields["x-netscan-customeraccountid"] = netscan_customer_account_id
    if not user_id_matcher.match(netscan_user_id):
        invalid_fields["x-netscan-userid"] = netscan_user_id

    if len(invalid_fields.keys()) > 0:
        body = {
            "errorMessage": "Malformed Request",
            "errorDetails": invalid_fields
        }
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {},
            "multiValueHeaders": {},
            "body": json.dumps(body)
        }

    # SEARCH FOR EXISTING USER #
    is_user_onboarded, response = WCaaSUtils.check_if_user_is_onboarded(netscan_customer_account_id, netscan_user_id)
    if not is_user_onboarded:
        body = json.dumps({
            "errorMessage": "Unauthorized",
            "errorDetails": f"Could not find user {netscan_user_id} under account {netscan_customer_account_id}.  "
                            f"Be sure to onboard before submitting a scan."
        })
        return RequestUtils.return_base64encoded_api_call(401, json.dumps(body))

    headers = {
        'x-netscan-customeraccountid': service_tenant_id,
        'x-netscan-userid': netscan_user_id,
        'content-type': 'application/json;charset=UTF-8'
    }

    # UPDATE SCHEDULE IN WCAAS
    table_name = "scheduled_scans"
    payload = {
        "timestamp": datetime.datetime.now().timestamp(),
        "whereClause": [
            f"schedule_id = '{schedule_id}'"
        ]
    }

    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/delete"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    status_code = response.status_code

    if status_code > 299:
        return {
            "isBase64Encoded": False,
            "statusCode": status_code,
            "headers": {},
            "multiValueHeaders": {},
            "body": json.dumps({
                "errorMessage": "Internal Server Error"
            })
        }

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "multiValueHeaders": {}
    }
