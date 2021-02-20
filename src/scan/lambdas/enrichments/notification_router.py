import boto3
import json
import re


def main(event, context):
    entries = []

    for _, record in enumerate(event.get("Records", [])):
        record["file_source"] = re.findall(r"(?:[^\/]+\/)*([^\/]+)\/[^\/]+", record['s3']['object']['key'])[0]
        record["enrichment_type"] = re.findall(r"(?:[^\/]+\/)?([^\/]+)\/.+", record['s3']['object']['key'])[0]

        # Remove trailing _SUCCESS and set key to root-level dir containing parquet info
        if record['s3']['object']['key'].endswith("_SUCCESS"):
            record['s3']['object']['key'] = record['s3']['object']['key'][:-8]

        entry = {
            'Source': 'cyberscan.sns',
            'Detail': json.dumps(record),
            'DetailType': 'Enrichment S3 PutObject Notification',
            'EventBusName': 'cyberscan-event-bus'
        }

        entries.append(entry)

    client = boto3.client('events')

    response = client.put_events(
        Entries=entries
    )

    return response
