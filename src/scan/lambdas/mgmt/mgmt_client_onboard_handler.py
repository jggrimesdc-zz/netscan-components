from __future__ import print_function

import datetime
import json
import uuid
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

    user_id = str(uuid.uuid4())
    netscan_customer_account_id, netscan_user_id = RequestUtils.extract_netscan_headers(event["headers"])

    # # SEARCH FOR EXISTING USER #
    is_user_onboarded, response = WCaaSUtils.check_if_user_is_onboarded(netscan_customer_account_id, netscan_user_id)
    if is_user_onboarded:
        return RequestUtils.return_base64encoded_api_call(302, json.dumps(response))

    # INSERT THE RECORD #
    status_code, body = WCaaSUtils.insert_new_user_record(netscan_customer_account_id, netscan_user_id, user_id,
                                                          datetime.datetime.now())
    return RequestUtils.return_base64encoded_api_call(status_code, json.dumps(body))
