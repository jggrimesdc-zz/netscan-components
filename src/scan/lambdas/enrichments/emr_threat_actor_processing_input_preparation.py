import json
import os
from scan_api_lib import SecretUtils


def main(event, context):
    bucket = os.environ.get("BUCKET")
    region = os.environ.get("AWS_REGION")
    rds_schema = os.environ.get("RDSHOST")

    dbconfig = json.loads(SecretUtils.get_secret("rds/wcaasmgmt", region)["SecretString"])

    event['detail']['sparkargs'] = []
    event['detail']['sparkargs'].append("spark-submit")
    event['detail']['sparkargs'].append(f"s3://{bucket}/scripts/emr_threat_actor_processor.py")
    event['detail']['sparkargs'].append("--bucketName")
    event['detail']['sparkargs'].append(event["detail"].get("s3", {}).get("bucket", {}).get("name"))
    event['detail']['sparkargs'].append("--objectKey")
    event['detail']['sparkargs'].append(event["detail"].get("s3", {}).get("object", {}).get("key"))
    event['detail']['sparkargs'].append("--fileSource")
    event['detail']['sparkargs'].append(event["detail"].get("file_source"))
    event['detail']['sparkargs'].append("--rdsDB")
    event['detail']['sparkargs'].append(dbconfig["username"])
    event['detail']['sparkargs'].append("--rdsHost")
    event['detail']['sparkargs'].append(dbconfig["host"])
    event['detail']['sparkargs'].append("--rdsSchema")
    event['detail']['sparkargs'].append(rds_schema)
    event['detail']['sparkargs'].append("--rdsUsername")
    event['detail']['sparkargs'].append(dbconfig["username"])
    event['detail']['sparkargs'].append("--rdsPassword")
    event['detail']['sparkargs'].append(dbconfig["password"])

    return event
