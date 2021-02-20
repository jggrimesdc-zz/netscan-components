from __future__ import print_function

import json
import os
import requests

print('Loading function')


def value_switch(path_param, value_param):
    valuelist = {
        "ssl": {
            "table": "external_reputation_by_ssl_sha",
            "where_stmt": f"ssl_sha ='{value_param}'"
        },
        "ip": {
            "table": "external_reputation_by_ip",
            "where_stmt": f"ip ='{value_param}'"
        },
        "domain": {
            "table": "external_reputation_by_domain",
            "where_stmt": f"domain ='{value_param}'"
        }
    }

    return valuelist.get(path_param.lower(), None)


def is_digit(value_param):
    try:
        int(value_param)
        return True
    except ValueError:
        return False


def lambda_handler(event, context):
    # INITIALIZE ENVIRONMENT #
    print(event)
    event = json.loads(json.dumps(event))
    service_tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID")
    service_user_id = os.environ.get("WCAAS_SERVICE_USER_ID")
    cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID")
    crud_api_url = os.environ.get("CRUD_API_URL")
    enrichments_keyspace_id = os.environ.get("ENRICHMENTS_KEYSPACE")

    headers = {
        'X-netscan-CustomerAccountId': service_tenant_id,
        'X-netscan-UserId': service_user_id,
        'content-type': 'application/json;charset=UTF-8',
        'X-API-VERSION': '2'
    }

    path = event["queryStringParameters"]["path"]
    val = event["queryStringParameters"]["value"]

    limit = event["queryStringParameters"].get("limit")
    page = event["queryStringParameters"].get("page")
    per_page = event["queryStringParameters"].get("per_page")

    # determine table name

    # SEARCH FOR EXISTING USER #

    rval = value_switch(path, val)
    if rval is None:
        return {
            "isBase64Encoded": False,
            "statusCode": 204,
            "headers": {},
            "multiValueHeaders": {},
            "body": "Invalid Query Path"
        }

    table_name = rval['table']

    print(table_name)
    print(rval['where_stmt'])

    does_user_exist_json = {
        "allowFiltering": True,
        "consistencyLevel": "LOCAL_QUORUM",
        "distinct": False,
        "perPartitionLimit": 10,
        "selectClause": [
            "*"
        ],
        "whereClause": [
            f"{rval['where_stmt']}"
        ]
    }

    if limit is not None and is_digit(limit):
        does_user_exist_json.update({"limit": int(limit)})

    print(does_user_exist_json)

    endpoint = f"api/clusters/{cluster_id}/keyspaces/{enrichments_keyspace_id}/tables/{table_name}/select"

    print(endpoint)
    print(f"{crud_api_url}/{endpoint}")

    query_params = {}
    if page is not None and is_digit(page):
        query_params.update({"page": int(page)})

    if per_page is not None and is_digit(per_page):
        query_params.update({"per_page": int(per_page)})

    response = requests.post(f"{crud_api_url}/{endpoint}",
                             data=json.dumps(does_user_exist_json),
                             headers=headers,
                             params=query_params)
    status_code = response.status_code

    if status_code != 200:
        return {
            "isBase64Encoded": False,
            "statusCode": status_code,
            "headers": {},
            "multiValueHeaders": {},
            "body": json.dumps({
                "errorMessage": "CRUD API Error",
                "errorDetails": f"Error retrieving data from the CRUD API.  "
                                f"Response: {response.content}"
            })
        }

    response_str = response.content.decode('utf-8')
    if response_str is None or response_str == "[]":
        status_code = 204
        response_body = "No Data"
    else:
        response_obj = json.loads(response_str)
        for _, obj in enumerate(response_obj["items"]):
            obj["timestamp"] = obj["timestamp"].replace(" ", "T")
        response_body = json.dumps(response_obj)

    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {},
        "multiValueHeaders": {},
        "body": response_body
    }
