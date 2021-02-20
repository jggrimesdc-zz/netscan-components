from __future__ import print_function

import datetime
import json
from scan_api_lib import EnvironmentSourcer
from scan_api_lib import LoggingUtils
from scan_api_lib import RequestUtils
from scan_api_lib import SQSUtils
from scan_api_lib import StatusChanger
from scan_api_lib import WCaaSUtils

print('Loading function')


def handle(event, context):
    # region PULL FROM SQS QUEUE
    response = SQSUtils.poll_scan("us-east-2", EnvironmentSourcer.scan_submission_queue())
    LoggingUtils.log_event("SQS_POP_SCAN", "INFO", "Scan popped from " + EnvironmentSourcer.scan_submission_queue())
    LoggingUtils.log_event("SQS_SCAN_RECORD", "INFO", "Scan popped from " + str(response))

    if len(response.keys()) == 0:
        return RequestUtils.return_base64encoded_api_call(204, json.dumps({
            "errorMessage": "No Content",
            "errorDetails": "Queue has no messages."
        }))
    receipt_handle = response['ReceiptHandle']
    if "MessageAttributes" not in response:
        return RequestUtils.return_base64encoded_api_call(204, json.dumps({
            "errorMessage": "No Content",
            "errorDetails": "This message is not relevant to CyberScan Polling.  Please try again or purge the "
                            "queue of invalid CyberScan messages and resubmit your scan request."
        }))

    scan_id = response['MessageAttributes']['scan_id']['StringValue']
    company_name = response['MessageAttributes']['name']['StringValue']
    duns = response['MessageAttributes']['duns']['StringValue']
    domains = response['MessageAttributes']['domains']['StringValue'].strip('][').replace("\"", "") \
        .replace("\'", "").split(', ')
    # endregion

    # region SEARCH FOR EXISTING SCAN
    is_user_onboarded, response = WCaaSUtils.check_if_scan_is_submitted(scan_id)
    if not is_user_onboarded and len(response) > 0:
        body = json.dumps({
            "errorMessage": f"Could not find scan record for scan_id {scan_id}",
            "errorDetails": f"Could not find scan record for scan_id {scan_id}.  Check the WCaaS Logs for details."
        })
        return RequestUtils.return_base64encoded_api_call(404, json.dumps(body))
    if not is_user_onboarded and len(response) == 0:
        body = json.dumps({
            "errorMessage": "No Content",
            "errorDetails": "User has not submitted a scan."
        })
        return RequestUtils.return_base64encoded_api_call(204, json.dumps(body))
    user_id = response["scan_user_id"]
    # endregion

    is_scan_count_present, check_current_scan_response = WCaaSUtils.check_current_scan_count(scan_id)
    if not is_scan_count_present:
        return RequestUtils.return_base64encoded_api_call(200, json.dumps({
            "errorMessage": f"Could not find scan record for scan_id {scan_id}",
            "errorDetails": f"Could not find scan record for scan_id {scan_id}.  Check the WCaaS Logs for details."
        }))

    new_event = {
        "detail": {
            "scan_id": str(scan_id),
            "company_name": company_name,
            "scan_user_id": str(user_id),
            "duns": duns,
            "domains": domains
        }
    }

    if "count" in check_current_scan_response:
        count = check_current_scan_response["count"]
        if count > int(EnvironmentSourcer.retry_count()):
            SQSUtils.delete_scan("us-east-2", EnvironmentSourcer.scan_submission_queue(), receipt_handle)
            SQSUtils.publish_failed_scan_message("us-east-2", scan_id, count)
            StatusChanger.publish_failed_status_updates(new_event)
        else:
            WCaaSUtils.insert_new_scan_count(scan_id, count + 1, datetime.datetime.now())
            StatusChanger.publish_retrying_status_updates(new_event)
            SQSUtils.delete_scan("us-east-2", EnvironmentSourcer.scan_submission_queue(), receipt_handle)
    else:
        WCaaSUtils.insert_new_scan_count(scan_id, 1, datetime.datetime.now())
        StatusChanger.publish_collecting_status_updates(new_event)
        SQSUtils.delete_scan("us-east-2", EnvironmentSourcer.scan_submission_queue(), receipt_handle)

    return RequestUtils.return_base64encoded_api_call(200, json.dumps({
        "scan_id": scan_id,
        "name": company_name,
        "domains": domains,
        "duns": duns
    }))
