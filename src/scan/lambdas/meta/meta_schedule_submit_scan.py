from __future__ import print_function

import boto3
import datetime
import json
import os
import requests
from scan_api_lib import LoggingUtils

tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID")
cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID")
crud_api_url = os.environ.get("CRUD_API_URL")
meta_data_keyspace_id = os.environ.get("META_DATA_KEYSPACE")
client = boto3.client('lambda')


def handle(event, context):
    LoggingUtils.log_event("SCHEDULE_SCAN_EVENT_PAYLOAD", "DEBUG", event)

    # sqs message body
    schedule = json.loads(event['Records'][0]['body'])

    # build request headers
    payload = {}
    payload['headers'] = {}
    payload['headers']['x-netscan-customeraccountid'] = schedule['customer_account_id']
    payload['headers']['x-netscan-userid'] = schedule['user_id']
    payload['body'] = {}
    payload['body']['force'] = True
    payload['body']['domains'] = json.loads(schedule['domains'])
    payload['body']['company_name'] = schedule['company_name']
    payload['body']['duns'] = schedule['duns']
    payload['body'] = json.dumps(payload['body'])

    LoggingUtils.log_event("SCHEDULE_SCAN_SUBMIT_REQUEST", "DEBUG", json.dumps(payload))

    response = client.invoke(
        FunctionName='cs_scan_submit',
        Payload=json.dumps(payload),
    )

    response_body = json.loads(response['Payload'].read().decode('utf-8'))

    LoggingUtils.log_event("SCHEDULE_SCAN_SUBMIT_RESPONSE", "DEBUG", response_body)

    response_status = response_body['statusCode']

    if response_status > 299:
        raise ValueError(f'cs_scan_submit returned a {response_status} status.', response_body)

    scan_id = json.loads(response_body['body'])['scan_id']
    scheduled_id = schedule['schedule_id']

    link_scan_id_to_schedule(scheduled_id, scan_id)

    return {
        'schedule_id': scheduled_id,
        'scan_id': scan_id
    }


def link_scan_id_to_schedule(schedule_id, scan_id):
    headers = {
        'X-netscan-CustomerAccountId': tenant_id,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    table_name = "scheduled_scan_history"
    insert_payload = {
        "consistencyLevel": "LOCAL_ONE",
        "ifNotExist": "false",
        "jsonClause": {
            "SCHEDULE_ID": schedule_id,
            "SCAN_ID": scan_id,
            "TIMESTAMP": str(datetime.datetime.now().isoformat(timespec='seconds'))
        },
        "timestamp": datetime.datetime.now().timestamp()
    }

    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/insert"
    requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(insert_payload), headers=headers)
