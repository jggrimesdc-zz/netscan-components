from __future__ import print_function

import datetime
import json
import os
import re
import requests
import uuid
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

    valid_headers, response_body = RequestUtils.validate_incoming_headers(event["headers"])
    if not valid_headers:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(response_body))

    request_body = json.loads(event['body'])

    invalid_fields = {}

    if "domains" not in request_body:
        invalid_fields["domains"] = "Not Present"
    if "company_name" not in request_body:
        invalid_fields["company_name"] = "Not Present"
    if "duns" not in request_body:
        invalid_fields["duns"] = "Not Present"
    if "recurrence" not in request_body:
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

    company_name = request_body['company_name']
    domains = request_body['domains']
    domains.sort()
    duns = str(request_body['duns'])
    recurrence = str(request_body['recurrence'])

    if "next_scheduled_run" in request_body:
        try:
            next_scheduled_run = parse_date(request_body['next_scheduled_run'])
        except Exception:
            invalid_fields["next_scheduled_run"] = request_body['next_scheduled_run']
    else:
        next_scheduled_run = next_occurrence(datetime.datetime.now(), recurrence)

    netscan_customer_account_id = str(event["headers"]["x-netscan-customeraccountid"]).strip()
    netscan_user_id = str(event["headers"]["x-netscan-userid"]).strip()
    user_id_matcher = re.compile("^[a-zA-Z0-9_]+$")
    domain_matcher = re.compile(r"(//|\s+|^)(\w\.|\w[A-Za-z0-9-]{0,61}\w\.){1,3}[A-Za-z]{2,6}")
    is_company_name_str = isinstance(company_name, str)
    if not is_company_name_str:
        invalid_fields["company_name"] = company_name
    if not company_name:
        invalid_fields["company_name"] = company_name
    if type(domains) is list:
        for domain in domains:
            if not domain_matcher.match(domain):
                invalid_fields["domains"] = domains
                break
    else:
        invalid_fields["domains"] = domains
    if not duns.isdigit():
        invalid_fields["duns"] = duns
    if not user_id_matcher.match(netscan_customer_account_id):
        invalid_fields["x-netscan-customeraccountid"] = netscan_customer_account_id
    if not user_id_matcher.match(netscan_user_id):
        invalid_fields["x-netscan-userid"] = netscan_user_id
    if recurrence and recurrence not in ["daily", "weekly", "monthly", "quarterly"]:
        invalid_fields["recurrence"] = recurrence

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

    # SEARCH FOR EXISTING USER #
    is_user_onboarded, response = WCaaSUtils.check_if_user_is_onboarded(netscan_customer_account_id, netscan_user_id)
    if not is_user_onboarded:
        response_body = json.dumps({
            "errorMessage": "Unauthorized",
            "errorDetails": f"Could not find user {netscan_user_id} under account {netscan_customer_account_id}.  "
                            f"Be sure to onboard before submitting a scan."
        })
        return RequestUtils.return_base64encoded_api_call(401, json.dumps(response_body))

    user_id = response["scan_user_id"]

    headers = {
        'x-netscan-customeraccountid': service_tenant_id,
        'x-netscan-userid': netscan_user_id,
        'content-type': 'application/json;charset=UTF-8'
    }

    # SEARCH FOR EXISTING SCHEDULE #
    str_domains = str(domains).replace("\'", "\"")
    table_name = "scheduled_scans"

    payload = {
        "allowFiltering": True,
        "consistencyLevel": "LOCAL_ONE",
        "distinct": False,
        "selectClause": [
            "*"
        ],
        "whereClause": [
            f"scan_user_id = '{user_id}'",
            f"domains = '{str_domains}'"
        ]
    }

    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/select"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    response_str = response.content.decode('utf-8')
    response_obj = json.loads(response_str)

    if len(response_obj) > 0:
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {},
            "multiValueHeaders": {},
            "body": json.dumps({
                "message": "Scheduled scan already exists for domain(s).",
                "schedule_id": response_obj[0]["schedule_id"],
                "next_scheduled_run": str(next_scheduled_run.isoformat(timespec='seconds'))
            })
        }

    schedule_id = uuid.uuid4()

    # STORE SCAN REQUEST IN WCAAS
    table_name = "scheduled_scans"
    payload = {
        "consistencyLevel": "LOCAL_ONE",
        "ifNotExist": "false",
        "jsonClause": {
            "SCHEDULE_ID": str(schedule_id),
            "SCAN_USER_ID": user_id,
            "USER_ID": netscan_user_id,
            "CUSTOMER_ACCOUNT_ID": netscan_customer_account_id,
            "RECURRENCE": recurrence,
            "COMPANY_NAME": company_name,
            "DUNS": str(duns),
            "DOMAINS": str(str_domains),
            "NEXT_SCHEDULED_RUN": str(next_scheduled_run.isoformat(timespec='seconds')),
            "CREATED_ON": str(datetime.datetime.now().isoformat(timespec='seconds')),
        },
        "timestamp": datetime.datetime.now().timestamp()
    }
    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/insert"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    insert_scan_status_code = response.status_code
    insert_scan_body = json.loads(response.content.decode('utf-8'))
    insert_scan_body = json.dumps(insert_scan_body).replace("\"[", "[").replace("]\"", "]").replace("\'", "\"")
    if insert_scan_status_code == 500:
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
