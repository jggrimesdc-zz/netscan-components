from __future__ import print_function

import json
from scan_api_lib import RequestUtils
from scan_api_lib import StatusChanger
from scan_api_lib import WCaaSUtils

print('Loading function')


def lambda_handler(event, context):
    event = json.loads(json.dumps(event))

    valid_path_parameters, body = RequestUtils.validate_scanid_path_parameter(event["pathParameters"])
    if not valid_path_parameters:
        return RequestUtils.return_base64encoded_api_call(400, json.dumps(body))
    scan_id = event["pathParameters"]["scan_id"]

    is_scan_real, response = WCaaSUtils.get_scan_meta_data(scan_id)
    if not is_scan_real:
        body = json.dumps({
            "errorMessage": "Scan Not Found",
            "errorDetail": f"Could not find data for scan_id {scan_id}.  Are you sure that is the correct ID?"
        })
        return RequestUtils.return_base64encoded_api_call(404, json.dumps(body))

    event = {
        "detail": {
            "scan_id": scan_id,
            "scan_user_id": response["scan_user_id"],
            "company_name": response["company_name"],
            "duns": response["duns"],
            "domains": response["domain"]
        }
    }

    StatusChanger.publish_invaildated_status_updates(event)
    return RequestUtils.return_base64encoded_api_call(200, json.dumps({}))
