from __future__ import print_function

import json
from scan_api_lib import RequestUtils
from scan_api_lib import WCaaSUtils

print('Loading function')


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))

    # VALIDATE INPUT #
    valid_headers, body = RequestUtils.validate_incoming_headers(event["headers"])
    if not valid_headers:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(body))

    valid_path_parameters, body = RequestUtils.validate_scanid_path_parameter(event["pathParameters"])
    if not valid_path_parameters:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(body))

    scan_id = event["pathParameters"]["scan_id"]
    netscan_customer_account_id, netscan_user_id = RequestUtils.extract_netscan_headers(event["headers"])

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
    status_code, body = WCaaSUtils.get_status_by_scan_id_for_scan_user(scan_id, user_id)
    return RequestUtils.return_base64encoded_api_call(status_code, json.dumps(body))
