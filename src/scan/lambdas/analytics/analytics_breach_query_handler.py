from __future__ import print_function

import copy
import json
import os
import requests
from scan_api_lib import LoggingUtils, RequestUtils


def value_switch(path_param, value_params):
    valuelist = {
        "email": {
            "table": "external_breach_by_email",
            "where_stmt": f"email ='{value_params.get('email')}'"
        },
        "pass": {
            "table": "external_breach_by_pass",
            "where_stmt": f"pass ='{value_params.get('pass')}'"
        },
        "pass_character_set": {
            "table": "external_breach_by_pass_character_set",
            "where_stmt": f"pass_character_set ='{value_params.get('character_set')}'"
        },
        "pass_complexity": {
            "table": "external_breach_by_pass_complexity",
            "where_stmt": (f"pass_complexity_digit = {value_params.get('digit')} "
                           f"AND pass_complexity_lower = {value_params.get('lower')} "
                           f"AND pass_complexity_upper = {value_params.get('upper')} "
                           f"AND pass_complexity_special = {value_params.get('special')} "
                           )
        },
        "pass_length": {
            "table": "external_breach_by_pass_length",
            "where_stmt": f"pass_length = {value_params.get('length')}"
        },
        "domain": {
            "table": "external_breach_by_domain",
            "where_stmt": f"domain = '{value_params.get('domain')}'"
        },
        "domain_pass_advanced_mask": {
            "table": "external_breach_by_domain_pass_advanced_mask",
            "groupby": "domain",
            "where_stmt": (f"pass_advanced_mask = '{value_params.get('advanced_mask')}' "
                           f"AND domain = '{value_params.get('domain')}'"
                           )
        },
        "domain_pass_character_set": {
            "table": "external_breach_by_domain_pass_character_set",
            "where_stmt": (f"pass_character_set = '{value_params.get('character_set')}' "
                           f"AND domain = '{value_params.get('domain')}'"
                           )
        },
        "domain_pass_complexity": {
            "table": "external_breach_by_domain_pass_complexity",
            "where_stmt": (f"domain = '{value_params.get('domain')}' "
                           f"AND pass_complexity_digit = {value_params.get('digit')} "
                           f"AND pass_complexity_lower = {value_params.get('lower')} "
                           f"AND pass_complexity_upper = {value_params.get('upper')} "
                           f"AND pass_complexity_special = {value_params.get('special')} "
                           )
        },
        "domain_pass_length": {
            "table": "external_breach_by_domain_pass_length",
            "where_stmt": (f"pass_length = {value_params.get('length')} "
                           f"AND domain = '{value_params.get('domain')}'"
                           )
        },
        "domain_pass_simple_mask": {
            "table": "external_breach_by_domain_pass_simple_mask",
            "where_stmt": (f"pass_simple_mask = '{value_params.get('simple_mask')}' "
                           f"AND domain = '{value_params.get('domain')}'"
                           )
        }
    }

    return valuelist.get(path_param.lower(), None)


def get_validation_dict():
    return {
        'email': {
            'email': 'string_val'
        },
        'pass': {
            'pass': 'string_val'
        },
        'pass_character_set': {
            'character_set': 'string_val'
        },
        'pass_complexity': {
            'digit': 0,
            'lower': 0,
            'upper': 0,
            'special': 0
        },
        'pass_length': {
            'length': 0
        },
        'domain': {
            'domain': 'string_val'
        },
        'domain_pass_advanced_mask': {
            'domain': 'string_val',
            'advanced_mask': 'string_val'
        },
        'domain_pass_character_set': {
            'domain': 'string_val',
            'character_set': 'string_val'
        },
        'domain_pass_complexity': {
            'domain': 'string_val',
            'digit': 0,
            'lower': 0,
            'upper': 0,
            'special': 0
        },
        'domain_pass_length': {
            'domain': 'string_val',
            'length': 0
        },
        'domain_pass_simple_mask': {
            'domain': 'string_val',
            'simple_mask': 'string_val'
        }
    }


def is_digit(value_param):
    try:
        int(value_param)
        return True
    except ValueError:
        return False


def get_object_types(query_values):
    new_dict = query_values
    for key in new_dict:
        new_dict[key] = type(new_dict[key])
    return new_dict


def lambda_handler(event, context):
    # INITIALIZE ENVIRONMENT #

    # log the lambda input payload
    LoggingUtils.log_event("BREACH_API_LAMBDA_EVENT", "INFO", event)

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

    # get dictionary for breach table query value validation
    table_validation = get_validation_dict()
    event_copy = copy.deepcopy(event)

    # initialize an empty dictionary to start appending request input params
    input_vals = {}

    # VALIDATE INPUT
    invalid_fields = {}
    if "path" not in event["queryStringParameters"]:
        invalid_fields["path"] = "Not Present"
    else:
        # iterate through the remainder input values
        for key in event_copy["queryStringParameters"]:
            if key not in 'limit' and key not in 'page' and key not in 'per_page' and key not in 'path':
                input_vals[key] = event_copy["queryStringParameters"][key]

        path = event["queryStringParameters"]["path"]
        valid_vals = table_validation[path]

        # sort the lists to compare for equality
        valid_vals = get_object_types(valid_vals)
        input_vals = get_object_types(input_vals)

        if valid_vals != input_vals:
            invalid_fields["values"] = (
                f"Incorrect query values; expected"
                f"{valid_vals}, got {input_vals}"
            )

    if len(invalid_fields.keys()) > 0:
        body = {
            "errorMessage": "Malformed Request",
            "errorDetails": invalid_fields
        }
        return RequestUtils.return_base64encoded_api_call(400, str(body))

    path = event["queryStringParameters"]["path"]
    values = {}
    for key in event["queryStringParameters"]:
        if key not in 'limit' and key not in 'page' and key not in 'per_page' and key not in 'path':
            values[key] = event["queryStringParameters"][key]

    page = event["queryStringParameters"].get("page")
    per_page = event["queryStringParameters"].get("per_page")

    rval = value_switch(path, values)
    if rval is None:
        return RequestUtils.return_base64encoded_api_call(204, "Invalid Query Path")

    table_name = rval['table']

    does_user_exist_json = {
        "allowFiltering": False,
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

    endpoint = (
        f"api/clusters/{cluster_id}/keyspaces/"
        f"{enrichments_keyspace_id}/tables/{table_name}/select"
    )

    query_params = {}
    if page is not None and is_digit(page):
        query_params.update({"page": int(page)})

    if per_page is not None and is_digit(per_page):
        query_params.update({"per_page": int(per_page)})

    # log the wcaas request body
    LoggingUtils.log_event("BREACH_WCAAS_REQUEST_BODY", "INFO", does_user_exist_json)

    # log the wcaas request extra parameters
    LoggingUtils.log_event("BREACH_WCAAS_REQUEST_QUERY_PARAMS", "INFO", query_params)

    response = requests.post(f"{crud_api_url}/{endpoint}",
                             data=json.dumps(does_user_exist_json),
                             headers=headers,
                             params=query_params)

    status_code = response.status_code

    # log the wcaas request body
    LoggingUtils.log_event("BREACH_WCAAS_RESPONSE_BODY", "INFO", response)

    # log the wcaas request extra parameters
    LoggingUtils.log_event("BREACH_WCAAS_RESPONSE_CODE", "INFO", status_code)

    if status_code != 200:
        return RequestUtils.return_base64encoded_api_call(
            status_code,
            json.dumps({
                "errorMessage": "CRUD API Error",
                "errorDetails": f"Error retrieving data from the CRUD API.  "
                                f"Response: {response.content}"
            })
        )

    response_str = response.content.decode('utf-8')
    if response_str is None or response_str == "[]":
        status_code = 204
        response_body = "No Data"
    else:
        response_obj = json.loads(response_str)
        for _, obj in enumerate(response_obj["items"]):
            obj["timestamp"] = obj["timestamp"].replace(" ", "T")
        response_body = json.dumps(response_obj)

    return RequestUtils.return_base64encoded_api_call(
        status_code,
        response_body
    )
