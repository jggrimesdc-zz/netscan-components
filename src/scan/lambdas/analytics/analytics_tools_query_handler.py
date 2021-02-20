from __future__ import print_function

import copy
import json
import os
import psycopg2
from math import isnan
from scan_api_lib import SecretUtils, LoggingUtils, RequestUtils


def get_validation_dict():
    return {
        'name': {
            'name': 'string_val'
        },
        'type': {
            'category': 'string_val'
        },
        'ttp_id': {
            'external_id': 'string_val'
        }
    }


def get_object_types(query_values):
    new_dict = query_values
    for key in new_dict:
        new_dict[key] = type(new_dict[key])
    return new_dict


def lambda_handler(event, context):
    # log the lambda input payload
    LoggingUtils.log_event("TOOLS_API_LAMBDA_EVENT", "INFO", event)

    secret_name = os.environ.get("DB_SECRET_NAME")
    region = os.environ.get("AWS_REGION")
    dbconfig = json.loads(SecretUtils.get_secret(secret_name, region)["SecretString"])

    # Attempt to connect to RDS instance
    try:
        conn = psycopg2.connect(dbname="wcaasmgmt",
                                user=dbconfig["username"],
                                password=dbconfig["password"],
                                host=dbconfig["host"])
    except psycopg2.OperationalError as e:
        LoggingUtils.log_event(
            "TOOLS_API_LAMBDA_PG_ERROR",
            "ERROR",
            'Unexpected error: Could not connect to PostgreSQL instance.'
        )

        body = {
            "errorMessage": "RDS Connection Error",
            "errorDetails": f"Error connecting to the RDS instance.  "
                            f"Response: {e}"
        }
        return RequestUtils.return_base64encoded_api_call(500, str(body))

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
            if key not in 'limit' and \
                    key not in 'page' and \
                    key not in 'per_page' and \
                    key not in 'path':
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
    page_val = event["queryStringParameters"].get("page") or "1"
    per_page_val = event["queryStringParameters"].get("per_page") or "50"

    page = int(page_val) if page_val.isnumeric() else 1
    per_page = int(per_page_val) if per_page_val.isnumeric() else 50

    values = {}

    for key in event["queryStringParameters"]:
        if key not in 'limit' and key not in 'page' and key not in 'per_page' and key not in 'path':
            values[key] = event["queryStringParameters"][key]

    query = ""
    if path in ('name', 'type'):
        query += "SELECT * FROM tool.tools_summary_view"
        if 'name' in values:
            query += " WHERE tool.tools_summary_view.\"NAME\" = %s"
            execution_params = [query, (values['name'])]
        if 'category' in values:
            query += " WHERE %s = ANY (tool.tools_summary_view.\"CATEGORY\")"
            execution_params = [query, (values['category'])]
        columns = (
            'name',
            'category',
            'description',
            'package_url',
            "source_of_tool",
            "external_id",
            "external_url"
        )
    else:
        query += "SELECT * FROM tool.ttp_tools_relationship_view"
        query += " WHERE tool.ttp_tools_relationship_view.\"tactic_external_id\" = %s"
        execution_params = [query, (str(values['external_id']))]
        columns = (
            'tactic_external_id',
            'tactic_name',
            'type',
            'tactic_external_url',
            'tactics',
            'name',
            'category',
            'description',
            'package_url',
            "source_of_tool",
            "software_external_id",
            "software_external_url",
            'target_type',
            'relationship_type'
        )

    # add pagination to the query
    tmp = [execution_params[1]]
    tmp.append((page - 1) * per_page)
    tmp.append(per_page + 1)
    execution_params[1] = tuple(tmp)
    execution_params[0] += " OFFSET %s LIMIT %s"

    # log the postgres query
    LoggingUtils.log_event("TOOLS_API_POSTGRES_QUERY", "INFO", query)

    rows = []
    with conn.cursor() as cur:
        cur.execute(*execution_params)
        try:
            rows = cur.fetchall()
        except psycopg2.ProgrammingError as e:
            LoggingUtils.log_event(
                "TOOLS_API_LAMBDA_PG_ERROR",
                "ERROR",
                'Unexpected error: Could not execute query.'
            )
            body = {
                "errorMessage": "Postgres Programming Error",
                "errorDetails": f"Error executing the following query: \"{query}\".  "
                                f"Response: {e}"
            }
            return RequestUtils.return_base64encoded_api_call(500, str(body))

    # log the postgres response
    LoggingUtils.log_event("TOOLS_API_POSTGRES_RESPONSE", "INFO", str(rows))

    results = {
        "meta": {},
        "items": []
    }

    results["meta"]["hasMore"] = len(rows[per_page:]) >= 1

    for row in rows[:per_page]:
        raw_row = json.loads(json.dumps(row, indent=4, sort_keys=True, default=str))

        # Replace invalid json values with defaults - float(NaN) defaults to 0
        cleaned_row = [0 if (isinstance(x, float) and isnan(x)) else x for x in raw_row]
        results["items"].append(dict(zip(columns, cleaned_row)))

    response_body = json.dumps(results)
    if len(results["items"]) == 0:
        status_code = 204
    else:
        status_code = 200

    return RequestUtils.return_base64encoded_api_call(status_code, str(response_body))
