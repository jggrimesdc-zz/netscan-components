from __future__ import print_function

import json
import os
import requests
from scan_api_lib import RequestUtils
from scan_api_lib import WCaaSUtils

service_tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID")
cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID")
crud_api_url = os.environ.get("CRUD_API_URL")
meta_data_keyspace_id = os.environ.get("META_DATA_KEYSPACE")
mgmt_keyspace_id = os.environ.get("MGMT_DATA_KEYSPACE")


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))

    # VALIDATE INPUT #
    request_headers = event["headers"]

    # Validate headers
    valid_headers, response_body = RequestUtils.validate_incoming_headers(request_headers)
    if not valid_headers:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(response_body))

    netscan_customer_account_id = str(request_headers["x-netscan-customeraccountid"]).strip()
    netscan_user_id = str(request_headers["x-netscan-userid"]).strip()
    schedule_id = ""
    recurrence = ""

    if event["pathParameters"]:
        schedule_id = event["pathParameters"].get("schedule_id", None)

    if event["queryStringParameters"]:
        recurrence = event["queryStringParameters"].get("recurrence", None)

    # SEARCH FOR EXISTING USER #
    is_user_onboarded, response = WCaaSUtils.check_if_user_is_onboarded(netscan_customer_account_id, netscan_user_id)
    if not is_user_onboarded:
        body = json.dumps({
            "errorMessage": "Unauthorized",
            "errorDetails": f"Could not find user {netscan_user_id} under account {netscan_customer_account_id}.  "
                            f"Be sure to onboard before submitting a scan."
        })
        return RequestUtils.return_base64encoded_api_call(401, json.dumps(body))

    user_id = response["scan_user_id"]

    payload = {
        "allowFiltering": True,
        "consistencyLevel": "LOCAL_ONE",
        "distinct": False,
        "selectClause": [
            "*"
        ],
        "whereClause": [
            f"scan_user_id = '{user_id}'"
        ]
    }

    if schedule_id:
        payload['whereClause'].append(f"schedule_id = '{schedule_id}'")
    elif recurrence:
        payload['whereClause'].append(f"recurrence = '{recurrence}'")

    table_name = "scheduled_scans"
    headers = {
        'x-netscan-customeraccountid': service_tenant_id,
        'x-netscan-userid': netscan_user_id,
        'content-type': 'application/json;charset=UTF-8'
    }

    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/select"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    response_str = response.content.decode('utf-8')
    response_obj = json.loads(response_str)
    response_body = list(map(schedule_response_item, response_obj))

    if schedule_id:
        if len(response_body) > 0:
            response_body = response_body[0]
        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": {},
                "multiValueHeaders": {},
                "body": json.dumps({
                    "message": "Schedule not found."
                })
            }

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "multiValueHeaders": {},
        "body": json.dumps(response_body)
    }


def schedule_response_item(schedule):
    return {
        'schedule_id': schedule['schedule_id'],
        'recurrence': schedule['recurrence'],
        'domains': json.loads(schedule['domains']),
        'company_name': schedule['company_name'],
        'duns': schedule['duns'],
        'created_on': schedule['created_on'],
        'next_scheduled_run': schedule['next_scheduled_run'],
        'last_scheduled_run': schedule['last_scheduled_run']
    }
