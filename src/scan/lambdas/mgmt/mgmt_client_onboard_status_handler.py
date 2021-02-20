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

    netscan_customer_account_id, netscan_user_id = RequestUtils.extract_netscan_headers(event["headers"])

    # SEARCH FOR EXISTING USER #
    is_user_onboarded, response = WCaaSUtils.check_if_user_is_onboarded(netscan_customer_account_id, netscan_user_id)
    if is_user_onboarded:
        return RequestUtils.return_base64encoded_api_call(200, json.dumps(response))

    return RequestUtils.return_api_call(404, json.dumps({
        "errorMessage": "Scan User not found in mgmt.client for given "
                        "Customer Account ID and User ID.  Try "
                        "onboarding first.",
        "errorDetails": {}
    })
                                        )
