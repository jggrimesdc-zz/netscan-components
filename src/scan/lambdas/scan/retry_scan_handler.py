from __future__ import print_function

import json
from scan_api_lib import RequestUtils, EnvironmentSourcer
from scan_api_lib import SQSUtils
from scan_api_lib import StatusChanger
from scan_api_lib import WCaaSUtils

print('Loading function')


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))

    # VALIDATE INPUT #
    valid_path_parameters, body = RequestUtils.validate_path_parameter(event["pathParameters"], "scan_id")
    if not valid_path_parameters:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(body))

    # SEARCH FOR EXISTING SCAN #
    scan_id = event["pathParameters"]["scan_id"]
    is_user_onboarded, response = WCaaSUtils.check_if_scan_is_submitted(scan_id)
    if not is_user_onboarded:
        body = json.dumps({
            "errorMessage": "Unauthorized",
            "errorDetails": f"Could not find scan object for scan_id {scan_id}."
        })
        return RequestUtils.return_base64encoded_api_call(401, json.dumps(body))

    scan_user_id = response["scan_user_id"]
    company_name = response["company_name"]
    duns = response["duns"]
    domains = response["domain"]

    # PUSH TO SQS QUEUE
    SQSUtils.publish_scan_to_sqs("us-east-2", EnvironmentSourcer.scan_submission_queue(), scan_id, company_name, duns,
                                 domains)

    new_event = {
        "detail": {
            "scan_id": str(scan_id),
            "company_name": company_name,
            "scan_user_id": str(scan_user_id),
            "duns": duns,
            "domains": domains
        }
    }
    StatusChanger.publish_retrying_status_updates(new_event)

    return RequestUtils.return_base64encoded_api_call(200, json.dumps({}))
