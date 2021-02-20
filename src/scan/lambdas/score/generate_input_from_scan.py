import datetime
import ipaddress
import json
import requests
import urllib.request as req
from scan_api_lib import EnvironmentSourcer as Env
from scan_api_lib import RequestUtils as ReqUtils
from scan_api_lib import S3Utils, EventBridgeUtils
from scan_api_lib import StatusChanger as Status


def get_unique_email_address(email_records, domain_list):
    unique_email_domains = {}
    for e in email_records:
        if "@" in e["email"]:
            domain_parts = e["email"].split("@")
            if len(domain_parts) > 1:
                unique_email_domains[domain_parts[1]] = True

    # if we didn't find any emails we assume that the inputs are primary domains
    # and should have spf, dmarc
    if len(unique_email_domains) == 0:
        for req_dom in domain_list:
            unique_email_domains[req_dom] = True

    return unique_email_domains


def check_cdn_list(ip_addr, cdn_list):
    present = False
    for cdn_ranges in cdn_list:
        if ipaddress.ip_address(ip_addr) in ipaddress.ip_network(cdn_ranges):
            present = True
        else:
            pass
    return present


def main(event, context):
    crud_api_url = Env.crud_api_url()
    cluster_id = Env.cluster_id()
    score_keyspace = Env.score_keyspace()
    headers = ReqUtils.get_headers()

    #######################
    # Store kickoff event #
    #######################
    EventBridgeUtils.publish_dqm_event(event)

    ########################
    # Update status tables #
    ########################
    Status.publish_scoring_status_updates(event)

    ##############################
    # Import CyberScan documents #
    ##############################
    request = S3Utils.get_file(event["detail"]["bucket_name"], event["detail"]["scan_id"] + "/meta.json")
    scan_records = S3Utils.get_file(event["detail"]["bucket_name"], event["detail"]["scan_id"] + "/raw/scan.json")
    email_records = S3Utils.get_file(event["detail"]["bucket_name"], event["detail"]["scan_id"] + "/raw/breach.json")
    dns_records = S3Utils.get_file(event["detail"]["bucket_name"], event["detail"]["scan_id"] + "/raw/dns.json")
    cdn_list = S3Utils.get_file_list(event["detail"]['bucket_name'], "prefix_cdns.txt")

    #####################
    # Process documents #
    #####################
    unique_email_domains = get_unique_email_address(email_records, request["domains"])

    spf_set = 0
    dmarc_set = 0
    browserv_set = 0
    browserv_total = 0
    common_open_ports = 0
    open_ports_total = 0
    headers_set = 0
    headers_total = 0
    https_set = 0

    for domain in dns_records:
        if dns_records[domain].get("spf", None) and dns_records[domain].get("dmarc", None):
            record = dns_records[domain]
            if len(record["spf"]["data"].keys()) > 0:
                spf_set = spf_set + 1
            if len(record["dmarc"]["data"].keys()) > 0:
                dmarc_set = dmarc_set + 1

    smtp_found = False
    for addr in scan_records:
        present = check_cdn_list(addr, cdn_list)
        if present:
            pass
        else:
            record = scan_records[addr]
            for port in record["ports"]:
                port = record["ports"][port]
                open_ports_total = open_ports_total + 1
                if port == "25" and port["protocol"] == "smtp":
                    if smtp_found:
                        open_ports_total = open_ports_total - 1
                    else:
                        common_open_ports = common_open_ports + 1
                        smtp_found = True
                elif port["common"]:
                    common_open_ports = common_open_ports + 1
                if port["name"] == "https" or port["name"] == "http" or port["name"] == "http-proxy":
                    browserv_total = browserv_total + 1
                    if "certificate" in port["tls"].keys():
                        https_set = https_set + 1
                    if port["tls"]["validation"]["browser_trusted"]:
                        browserv_set = browserv_set + 1
                    headers_set += port["headers"]["report"].get("total_pass", 0)
                    headers_total += port["headers"]["report"].get("total", 0)

    input_json = [{"signal": "spf", "total": len(unique_email_domains), "subset": spf_set},
                  {"signal": "dmarc", "total": len(unique_email_domains), "subset": dmarc_set},
                  {"signal": "browserv", "total": browserv_total, "subset": browserv_set},
                  {"signal": "https", "total": browserv_total, "subset": https_set},
                  {"signal": "op", "total": open_ports_total, "subset": common_open_ports},
                  {"signal": "wah", "total": headers_total, "subset": headers_set}]

    ####################################
    # Store generated input.json in s3 #
    ####################################
    S3Utils.put_file(
        event["detail"]["bucket_name"],
        f"{event['detail']['scan_id']}/report/input.json",
        json.dumps(input_json, separators=(',', ':'))
    )

    ######################################
    # Store input.json contents in WCAAS #
    ######################################
    input_payload = {
        "consistencyLevel": "LOCAL_ONE",
        "ifNotExist": "false",
        "jsonClause": {
            "SCAN_ID": event["detail"]["scan_id"],
            "USER_ID": event["detail"]["scan_user_id"],
            "TIMESTAMP": datetime.datetime.now().isoformat(timespec='seconds'),
            "SPF_TOTAL": input_json[0]["total"],
            "SPF_SUBSET": input_json[0]["subset"],
            "DMARC_TOTAL": input_json[1]["total"],
            "DMARC_SUBSET": input_json[1]["subset"],
            "BROWSERV_TOTAL": input_json[2]["total"],
            "BROWSERV_SUBSET": input_json[2]["subset"],
            "HTTPS_TOTAL": input_json[3]["total"],
            "HTTPS_SUBSET": input_json[3]["subset"],
            "OP_TOTAL": input_json[4]["total"],
            "OP_SUBSET": input_json[4]["subset"],
            "WAH_TOTAL": input_json[5]["total"],
            "WAH_SUBSET": input_json[5]["subset"],
            "S3_RAW_DUMP_URL": f"s3a://{event['detail']['bucket_name']}/{event['detail']['scan_id']}/report/input.json"
        },
        "timestamp": datetime.datetime.now().timestamp()
    }

    input_table = "score_input_spark_job_ab"
    input_endpoint = f"api/clusters/{cluster_id}/keyspaces/{score_keyspace}/tables/{input_table}/insert"
    requests.post(f"{crud_api_url}/{input_endpoint}", data=json.dumps(input_payload), headers=headers)

    new_domain_list = []
    domain_list = event["detail"]["domains"].replace("[\'", "").replace("\']", "").split(",")
    for domain in domain_list:
        new_domain_list.append(req.pathname2url(str(domain)))
    event["detail"]["domains"] = new_domain_list

    return event
