import datetime
import json
import requests
from scan_api_lib import EnvironmentSourcer as Env
from scan_api_lib import RequestUtils as ReqUtils
from scan_api_lib import S3Utils
from scan_api_lib import StatusChanger as Status


def get_default_report_objects(report):
    configuration_json = {}
    emd_json = {}
    poa_json = {}
    ts_json = {}
    controls = report["cyber_risk"]["controls"]
    for control in controls:
        name = control["name"]
        description = control["description"]
        weight = control["weight"]
        high_impact_control_score = control["high_impact_control_score"]
        medium_impact_control_score = control["medium_impact_control_score"]
        low_impact_control_score = control["low_impact_control_score"]
        new_json = {
            "name": name,
            "description": description,
            "weight": weight,
            "high_impact_control_score": high_impact_control_score,
            "medium_impact_control_score": medium_impact_control_score,
            "low_impact_control_score": low_impact_control_score
        }
        if name == "configuration":
            configuration_json = new_json
        elif name == "establish_maintain_documentation":
            emd_json = new_json
        elif name == "process_or_activity":
            poa_json = new_json
        elif name == "technical_security":
            ts_json = new_json
    return configuration_json, emd_json, poa_json, ts_json


def extract_score_report(event, report, ts_json, emd_json, configuration_json, poa_json):
    return {
        "consistencyLevel": "LOCAL_ONE",
        "ifNotExist": False,
        "jsonClause": {
            "SCAN_ID": event['detail']['scan_id'],
            "COMPANY_NAME": report["name"],
            "TIMESTAMP": datetime.datetime.now().isoformat(timespec='seconds'),
            "USER_ID": event["detail"]["scan_user_id"],
            "DUNS": event["detail"]["duns"],
            "RISK_SCORE": report["cyber_risk"]["score"],
            "RISK_IMPACT_HIGH": report["cyber_risk"]["high"],
            "RISK_IMPACT_HIGH_WGHT": report["cyber_risk"]["high_impact_weight"],
            "RISK_IMPACT_MED": report["cyber_risk"]["medium"],
            "RISK_IMPACT_MED_WGHT": report["cyber_risk"]["medium_impact_weight"],
            "RISK_IMPACT_LOW": report["cyber_risk"]["low"],
            "RISK_IMPACT_LOW_WGHT": report["cyber_risk"]["low_impact_weight"],
            "SGNLS_TECSEC_DESC": ts_json.get("description", "n/a"),
            "SGNLS_TECSEC_HIGH": ts_json.get("high_impact_control_score", "n/a"),
            "SGNLS_TECSEC_MED": ts_json.get("medium_impact_control_score", "n/a"),
            "SGNLS_TECSEC_LOW": ts_json.get("low_impact_control_score", "n/a"),
            "SGNLS_TECSEC_WGHT": ts_json.get("weight", "n/a"),
            "SGNLS_ESTMNTNDOC_DESC": emd_json.get("description", "n/a"),
            "SGNLS_ESTMNTNDOC_HIGH": emd_json.get("high_impact_control_score", "n/a"),
            "SGNLS_ESTMNTNDOC_MED": emd_json.get("medium_impact_control_score", "n/a"),
            "SGNLS_ESTMNTNDOC_LOW": emd_json.get("low_impact_control_score", "n/a"),
            "SGNLS_ESTMNTNDOC_WGHT": emd_json.get("weight", "n/a"),
            "SGNLS_CONF_DESC": configuration_json.get("description", "n/a"),
            "SGNLS_CONF_HIGH": configuration_json.get("high_impact_control_score", "n/a"),
            "SGNLS_CONF_MED": configuration_json.get("medium_impact_control_score", "n/a"),
            "SGNLS_CONF_LOW": configuration_json.get("low_impact_control_score", "n/a"),
            "SGNLS_CONF_WGHT": configuration_json.get("weight", "n/a"),
            "SGNLS_POA_DESC": poa_json.get("description", "n/a"),
            "SGNLS_POA_HIGH": poa_json.get("high_impact_control_score", "n/a"),
            "SGNLS_POA_MED": poa_json.get("medium_impact_control_score", "n/a"),
            "SGNLS_POA_LOW": poa_json.get("low_impact_control_score", "n/a"),
            "SGNLS_POA_WGHT": poa_json.get("weight", "n/a"),
            "S3_RAW_DUMP_URL": f"s3a://{event['detail']['bucket_name']}/{event['detail']['scan_id']}/report/report.json"
        },
        "timestamp": 0
    }


def main(event, context):
    crud_api_url = Env.crud_api_url()
    cluster_id = Env.cluster_id()
    score_keyspace = Env.score_keyspace()
    headers = ReqUtils.get_headers()

    #######################################
    # Retrieve report/report.json from S3 #
    #######################################
    report = S3Utils.get_file(
        event["detail"]["bucket_name"],
        event["detail"]["scan_id"] + "/report/report.json"
    )

    ################################
    # Define default report values #
    ################################
    configuration_json, emd_json, poa_json, ts_json = get_default_report_objects(report)

    ###########################
    # Put the report in WCAAS #
    ###########################
    payload = extract_score_report(event, report, ts_json, emd_json, configuration_json, poa_json)
    table_name = "score_report_lambda_job"
    endpoint = f"api/clusters/{cluster_id}/keyspaces/{score_keyspace}/tables/{table_name}/insert"
    requests.post(f"{crud_api_url}/{endpoint}", data=json.dumps(payload), headers=headers)

    ########################
    # Update status tables #
    ########################
    Status.publish_complete_status_updates(event)

    return event
