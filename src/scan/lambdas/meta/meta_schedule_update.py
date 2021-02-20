from __future__ import print_function

import datetime
import json
import os
import re
import requests
from dateutil.relativedelta import relativedelta
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
    body = json.loads(event['body'])
    headers = event["headers"]

    invalid_fields = {}

    if "x-netscan-customeraccountid" not in headers:
        invalid_fields["x-netscan-customeraccountid"] = "Not Present"
    if "x-netscan-userid" not in headers:
        invalid_fields["x-netscan-userid"] = "Not Present"

    if "recurrence" not in body:
        invalid_fields["recurrence"] = "Not Present"

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

    recurrence = str(body['recurrence'])

    if event["pathParameters"]:
        schedule_id = event["pathParameters"].get("schedule_id", None)

    next_scheduled_run = None

    if "next_scheduled_run" in body:
        try:
            next_scheduled_run = parse_date(body['next_scheduled_run'])
        except Exception:
            invalid_fields["next_scheduled_run"] = body['next_scheduled_run']

    if recurrence and not next_scheduled_run:
        next_scheduled_run = next_occurrence(datetime.datetime.now(), recurrence)

    netscan_customer_account_id = str(headers["x-netscan-customeraccountid"]).strip()
    netscan_user_id = str(headers["x-netscan-userid"]).strip()
    user_id_matcher = re.compile("^[a-zA-Z0-9_]+$")

    if not user_id_matcher.match(netscan_customer_account_id):
        invalid_fields["x-netscan-customeraccountid"] = netscan_customer_account_id
    if not user_id_matcher.match(netscan_user_id):
        invalid_fields["x-netscan-userid"] = netscan_user_id
    if recurrence and recurrence not in ["daily", "weekly", "monthly", "quarterly"]:
        invalid_fields["recurrence"] = recurrence

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
        "assignments": [],
        "timestamp": datetime.datetime.now().timestamp(),
        "whereClause": [
            f"schedule_id = '{schedule_id}'"
        ]
    }

    if recurrence:
        payload['assignments'].append(f"recurrence = '{recurrence}'")

    if next_scheduled_run:
        payload['assignments'].append(f"next_scheduled_run = '{str(next_scheduled_run.isoformat(timespec='seconds'))}'")

    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/update"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    insert_scan_status_code = response.status_code
    print(response.content.decode('utf-8'))
    if insert_scan_status_code == 500:
        insert_scan_body = json.loads(response.content.decode('utf-8'))
        insert_scan_body = json.dumps(insert_scan_body).replace("\"[", "[").replace("]\"", "]").replace("\'", "\"")
        return {
            "isBase64Encoded": False,
            "statusCode": 401,
            "headers": {},
            "multiValueHeaders": {},
            "body": json.dumps({
                "errorMessage": "Internal Server Error",
                "errorDetails": f"{insert_scan_body}"
            })
        }

    response_body = {}
    response_body["schedule_id"] = str(schedule_id).strip()
    response_body["next_scheduled_run"] = str(next_scheduled_run.isoformat(timespec='seconds'))

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "multiValueHeaders": {},
        "body": json.dumps(response_body)
    }


def add_months(sourcedate, months):
    return sourcedate + relativedelta(months=+months)


def add_days(sourcedate, days):
    return sourcedate + relativedelta(days=+days)


def next_occurrence(run_date, recurrence):
    if recurrence == "daily":
        return add_days(run_date, 1)
    if recurrence == "weekly":
        return add_days(run_date, 7)
    if recurrence == "monthly":
        return add_months(run_date, 1)
    if recurrence == "quarterly":
        return add_months(run_date, 3)
    raise ValueError('Unrecognized recurrence')


def parse_date(raw_date):
    if isinstance(raw_date, int):
        return datetime.datetime.utcfromtimestamp(raw_date)
    if isinstance(raw_date, str):
        return datetime.datetime.fromisoformat(raw_date)
    raise ValueError('Unrecognized date format')
