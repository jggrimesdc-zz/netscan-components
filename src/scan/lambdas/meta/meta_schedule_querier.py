from __future__ import print_function

import boto3
import datetime
import json
import os
import requests
from dateutil.relativedelta import relativedelta
from scan_api_lib import LoggingUtils

tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID")
cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID")
crud_api_url = os.environ.get("CRUD_API_URL")
meta_data_keyspace_id = os.environ.get("META_DATA_KEYSPACE")
scheduled_scans_queue_url = os.environ.get("SCHEDULED_SCANS_QUEUE_URL")

# parses aws region from the queue url
# ex. https://sqs.us-east-2.amazonaws.com/726764357059/ScheduledScans
region = scheduled_scans_queue_url.split('/')[2].split('.')[1]


def handle(event, context):
    # Get scan with given recurrence
    scheduled_scans = search_for_scheduled_scans()

    session = boto3.session.Session(region_name=region)
    sqs_client = session.client("sqs")

    LoggingUtils.log_event("SCHEDULE_SCAN_QUEUED", "INFO", f"Submitting {len(scheduled_scans)} scheduled scan(s).")

    # Submit each scheduled scan
    for schedule in scheduled_scans:
        success = submit_scan_to_sqs(sqs_client, schedule)

        if success:
            LoggingUtils.log_event("SCHEDULE_SCAN_QUEUED", "INFO", f"Queued {schedule['schedule_id']}")
        else:
            LoggingUtils.log_event("SCHEDULE_SCAN_QUEUED", "ERROR", f"Failed to queue {schedule['schedule_id']}")

    return event


def search_for_scheduled_scans():
    headers = {
        'X-netscan-CustomerAccountId': tenant_id,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    table_name = "scheduled_scans"
    does_user_exist_json = {
        "allowFiltering": True,
        "consistencyLevel": "LOCAL_ONE",
        "distinct": False,
        "selectClause": [
            "*"
        ],
        "whereClause": [
            f"NEXT_SCHEDULED_RUN <= '{str(datetime.datetime.now().isoformat(timespec='seconds'))}'"
        ]
    }
    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/select"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(does_user_exist_json), headers=headers)

    return json.loads(response.content.decode('utf-8'))


def submit_scan_to_sqs(sqs_client, schedule):
    sqs_client.send_message(
        QueueUrl=scheduled_scans_queue_url,
        MessageBody=json.dumps(schedule),
        MessageAttributes={
            'schedule_id': {
                'StringValue': str(schedule['schedule_id']),
                'DataType': 'String'
            }
        },
    )

    headers = {
        'x-netscan-customeraccountid': tenant_id,
        'x-netscan-userid': schedule['scan_user_id'],
        'content-type': 'application/json;charset=UTF-8'
    }

    table_name = "scheduled_scans"
    last_scheduled_run = datetime.datetime.now()
    next_scheduled_run = next_occurrence(last_scheduled_run, schedule['recurrence'])
    payload = {
        "assignments": [
            f"next_scheduled_run = '{str(next_scheduled_run.isoformat(timespec='seconds'))}'",
            f"last_scheduled_run = '{str(last_scheduled_run.isoformat(timespec='seconds'))}'"
        ],
        "timestamp": datetime.datetime.now().timestamp(),
        "whereClause": [
            f"schedule_id = '{schedule['schedule_id']}'"
        ]
    }
    endpoint = f"api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}/update"
    response = requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)
    return response.status_code < 300


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
