from __future__ import print_function

import json
from scan_api_lib import RequestUtils
from scan_api_lib import WCaaSUtils

print('Loading function')


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))

    # VALIDATE INPUT
    valid_parameters, body = RequestUtils.validate_incoming_dqm_eventlog_request(event["pathParameters"])
    if not valid_parameters:
        return RequestUtils.return_api_call(400, json.dumps(body))

    event_actor, event_action = RequestUtils.extract_dqm_path_parameters(event["pathParameters"])
    status_code, response = WCaaSUtils.select_dqm_records(event_actor, event_action)

    if response is None or response == "[]":
        status_code = 204

    return RequestUtils.return_api_call(status_code, response)
