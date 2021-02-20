from __future__ import print_function

import datetime
import json
import uuid
from scan_api_lib import RequestUtils, EnvironmentSourcer
from scan_api_lib import SQSUtils
from scan_api_lib import StatusChanger
from scan_api_lib import WCaaSUtils

print('Loading function')


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))

    # VALIDATE INPUT #
    valid_headers, body = RequestUtils.validate_incoming_headers(event["headers"])
    if not valid_headers:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(body))

    valid_body, body = RequestUtils.validate_incoming_scan_submission_body(json.loads(event["body"]))
    if not valid_body:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(body))

    netscan_customer_account_id, netscan_user_id = RequestUtils.extract_netscan_headers(event["headers"])
    body = json.loads(event["body"])
    company_name = body["company_name"]
    domains = body["domains"]
    duns = str(body["duns"])
    force = RequestUtils.is_scan_forced(body)

    # SEARCH FOR EXISTING USER #
    is_user_onboarded, response = WCaaSUtils.check_if_user_is_onboarded(netscan_customer_account_id, netscan_user_id)
    if not is_user_onboarded:
        body = json.dumps({
            "errorMessage": "Unauthorized",
            "errorDetails": f"Could not find user {netscan_user_id} under account {netscan_customer_account_id}.  "
                            f"Be sure to onboard before submitting a scan."
        })
        return RequestUtils.return_base64encoded_api_call(401, json.dumps(body))

    user_id = response["scan_user_id"]
    scan_id = uuid.uuid4()

    if not force:
        status_code, body = WCaaSUtils.select_cached_scan(domains)
        if status_code != 204:
            return RequestUtils.return_base64encoded_api_call(status_code, json.dumps(body))

    # STORE SCAN REQUEST IN WCAAS
    status_code, body = WCaaSUtils.insert_scan_input_metadata(scan_id, user_id, company_name, duns, domains,
                                                              datetime.datetime.now())
    if status_code > 499:
        error_body = {
            "errorMessage": "Internal Server Error",
            "errorDetails": body
        }
        return RequestUtils.return_base64encoded_api_call(401, json.dumps(error_body))

    SQSUtils.publish_scan_to_sqs("us-east-2", EnvironmentSourcer.scan_submission_queue(), scan_id, company_name, duns,
                                 domains)

    new_event = {
        "detail": {
            "scan_id": str(scan_id),
            "company_name": company_name,
            "scan_user_id": str(user_id),
            "duns": duns,
            "domains": domains
        }
    }
    StatusChanger.publish_queued_status_updates(new_event)

    # CACHED_SCAN
    status_code, body = WCaaSUtils.insert_new_cached_scan_record(datetime.datetime.now(), scan_id, domains)
    if status_code > 499:
        RequestUtils.return_base64encoded_api_call(status_code, json.dumps(body))

    response_body = {
        "scan_id": str(scan_id).strip(),
        "scan_status": "queued"
    }
    return RequestUtils.return_base64encoded_api_call(200, json.dumps(response_body))
