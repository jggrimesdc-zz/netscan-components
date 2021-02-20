from __future__ import print_function

import json
import os
import re
import requests
from urllib.parse import unquote

print('Loading function')


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))
    service_tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID", "dantenant")
    cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID", "1001")
    crud_api_url = os.environ.get("CRUD_API_URL")
    analytics_keyspace = os.environ.get("ANALYTICS_KEYSPACE", "analytics")

    # VALIDATE INPUT
    invalid_fields = {}
    if "domain" not in event["pathParameters"]:
        invalid_fields["company_name"] = "Not Present"
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
            "body": str(body)
        }

    path_param = event["pathParameters"]
    domain = unquote(path_param["domain"])
    domain_matcher = re.compile(r"(//|\s+|^)(\w\.|\w[A-Za-z0-9-]{0,61}\w\.){1,3}[A-Za-z]{2,6}")
    if not domain_matcher.match(event["pathParameters"]["domain"]):
        invalid_fields["domain"] = event["pathParameters"]["domain"]
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
            "body": str(body)
        }

    headers = {
        'X-netscan-CustomerAccountId': service_tenant_id,
        'X-netscan-UserId': "12345",
        'content-type': 'application/json;charset=UTF-8',
        'accept': '*/*'
    }
    payload = {
        "allowFiltering": "true",
        "consistencyLevel": "LOCAL_ONE",
        "distinct": "true",
        "groupByClause": "timestamp",
        "limit": 100,
        "orderingByClause": "timestamp ASC",
        "perPartitionLimit": 10,
        "selectClause": [
            "*"
        ],
        "whereClause": [
            f"domain_name = '{domain}'"
        ]
    }

    table_name = "by_domain"
    endpoint = f"api/clusters/{cluster_id}/keyspaces/{analytics_keyspace}/tables/{table_name}/select"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    response_obj = json.loads(response.content.decode('utf-8'))
    for _, obj in enumerate(response_obj):
        obj["timestamp"] = obj["timestamp"].replace(" ", "T")
    response_body = json.dumps(json.dumps(response_obj, separators=(",", ":")))

    return {
        "isBase64Encoded": False,
        "statusCode": response.status_code,
        "headers": {},
        "multiValueHeaders": {},
        "body": response_body
    }
