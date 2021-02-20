import os

bucket = os.environ.get("BUCKET")


def main(event, context):
    event['detail']['sparkargs'] = []
    event['detail']['sparkargs'].append("spark-submit")
    event['detail']['sparkargs'].append(f"s3://{bucket}/scripts/conform_breach_direct_to_s3.py")
    event['detail']['sparkargs'].append("--bucketName")
    event['detail']['sparkargs'].append(event["detail"].get("s3", {}).get("bucket", {}).get("name"))
    event['detail']['sparkargs'].append("--objectKey")
    event['detail']['sparkargs'].append(event["detail"].get("s3", {}).get("object", {}).get("key"))
    event['detail']['sparkargs'].append("--fileSource")
    event['detail']['sparkargs'].append(event["detail"].get("file_source"))

    return event
