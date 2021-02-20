# pylint: skip-file
from __future__ import print_function

import boto3
import datetime
import json
import os
import requests
from botocore.exceptions import ClientError
from scan_api_lib import StatusChanger as Status

print('Loading function')

headers = {
    'X-netscan-CustomerAccountId': f"{os.environ.get('WCAAS_SERVICE_TENANT_ID', 'dantenant')}",
    'X-netscan-UserId': "12345",
    'content-type': 'application/json;charset=UTF-8'
}


def handle(event, context):
    # INITIALIZE ENVIRONMENT #
    event = json.loads(json.dumps(event))
    exec_environ = os.environ.get("EXECUTION_ENVIRONMENT", "hosted")
    service_tenant_id = os.environ.get("WCAAS_SERVICE_TENANT_ID")
    cluster_id = os.environ.get("WCAAS_SERVICE_CLUSTER_ID")
    crud_api_url = os.environ.get("CRUD_API_URL")
    status_keyspace_id = os.environ.get("STATUS_KEYSPACE")
    dqm_keyspace_id = os.environ.get("DQM_KEYSPACE")
    netscan_customer_account_id = "dantenant"
    netscan_user_id = "12345"
    meta_data_keyspace_id = os.environ.get("META_DATA_KEYSPACE")
    scan_user_id = ""
    company_name = ""
    duns = ""
    domains = ""

    # PULL FROM S3 NEW OBJECT
    if exec_environ == "hosted":
        session = boto3.session.Session(region_name="us-east-2")
        s3_client = session.client("s3")
    else:
        session = boto3.session.Session(region_name="us-east-2", profile_name="netscan-dev")
        s3_client = session.client("s3")

    bucket = event['Records'][0]["s3"]["bucket"]["name"]
    key = event['Records'][0]["s3"]["object"]["key"]
    print(bucket)
    print(key)
    scan_id = str(key).split("/")[0]
    file_name = str(key).split("/")[-1]

    # STEP 1, GET SCAN_USER_ID FROM meta.scan_request_input TABLE
    print(file_name)
    if file_name == "breach.json":

        table_name = "request_input"
        # table_name = "request_input_temp"
        crud_url = f"{crud_api_url}/api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}" \
                   f"/select"
        print(crud_url)
        scan_user_id, company_name, duns, domains = get_scan_keys(crud_url, scan_id)
        if scan_user_id is "-1":
            print("return 404")
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": {},
                "multiValueHeaders": {},
                "body": {
                    "errorMessage": "Scan Not Found",
                    "errorDetail": f"Could not find data for scan_id {scan_id}.  Are you sure that is the correct ID?"
                }
            }

        status_event = {
            "detail": {
                "scan_id": str(scan_id),
                "company_name": company_name,
                "scan_user_id": str(scan_user_id),
                "duns": duns,
                "domains": domains
            }
        }
        Status.publish_serializing_status_updates(status_event)

        # STEP 2, WRITE META.JSON CONTENTS TO meta.meta_data TABLE
        table_name = "meta_data"
        key = f"{scan_id}/meta.json"
        try:
            obj = s3_client.get_object(Key=key, Bucket=bucket)
            contents = json.loads(obj['Body'].read())
            crud_url = f"{crud_api_url}/api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}" \
                       f"/insert"
            s3_url = f"https://{bucket}.s3.us-east-1.amazonaws.com/{key}"
            if contents is not None:
                store_meta_status_code, store_meta_response = store_meta_json(contents, crud_url, scan_user_id, s3_url)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                store_meta_status_code = ""
                store_meta_response = ""
                pass
            else:
                raise

        # STEP 3, WRITE BREACH.JSON CONTENTS TO meta.scan_breach_data TABLE
        table_name = "raw/breach_data"
        key = f"{scan_id}/raw/breach.json"
        try:
            obj = s3_client.get_object(Key=key, Bucket=bucket)
            contents = json.loads(obj['Body'].read())
            crud_url = f"{crud_api_url}/api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}" \
                       f"/tables/{table_name}/insert"
            s3_url = f"https://{bucket}.s3.us-east-1.amazonaws.com/{key}"
            if contents is not None:
                store_breach_status_code, store_breach_response = store_breach_json(contents, crud_url, scan_id,
                                                                                    scan_user_id, s3_url)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                store_breach_status_code = ""
                store_breach_response = ""
                pass
            else:
                raise

        # STEP 4, WRITE DNS.JSON CONTENTS TO meta.scan_dns_data TABLE
        table_name = "raw/dns_data"
        key = f"{scan_id}/raw/dns.json"
        try:
            obj = s3_client.get_object(Key=key, Bucket=bucket)
            contents = json.loads(obj['Body'].read())
            crud_url = f"{crud_api_url}/api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/{table_name}" \
                       f"/insert"
            s3_url = f"https://{bucket}.s3.us-east-1.amazonaws.com/{key}"
            if contents is not None:
                store_dns_status_code, store_dns_response = store_dns_json(contents, crud_url, scan_id, scan_user_id,
                                                                           s3_url)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                store_dns_status_code = ""
                store_dns_response = ""
                pass
            else:
                raise

        # STEP 5, WRITE SCAN.JSON CONTENTS TO meta.scan_scan_data TABLE
        # TODO Fix this input it's broke a.f.
        table_name = "raw/scan_data"
        key = f"{scan_id}/raw/scan.json"
        try:
            obj = s3_client.get_object(Key=key, Bucket=bucket)
            contents = json.loads(obj['Body'].read())
            s3_url = f"https://{bucket}.s3.us-east-1.amazonaws.com/{key}"
            crud_url = f"{crud_api_url}/api/clusters/{cluster_id}/keyspaces/{meta_data_keyspace_id}/tables/"
            if contents is not None:
                store_scan_status_code, store_scan_response = store_scan_json(contents, crud_url, scan_id, scan_user_id,
                                                                              s3_url)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                store_scan_status_code = ""
                store_scan_response = ""
                pass
            else:
                raise

        # STEP 7, UPDATE ALL OF THE STATUS TO "SCORING"
        new_event = {
            "detail": {
                "scan_id": scan_id,
                "company_name": company_name,
                "scan_user_id": scan_user_id,
                "duns": duns,
                "domains": domains
            }
        }
        # Status.publish_serializing_status_updates(new_event)

        # STEP 8, FIRE EVENTBRIDGE MESSAGE CONTAINING S3 FILE LOCATIONS
        times = datetime.datetime.now().isoformat(timespec='seconds')
        events = boto3.client('events')
        source = "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER"
        resources = ["CyberScan Collectors", "S3", "Lambda:ScanSerializer"]
        detail_type = "Trigger Downstream Analytics"
        detail = json.dumps({
            "bucket_name": bucket,
            "scan_id": scan_id,
            "scan_user_id": scan_user_id,
            "duns": duns,
            "domains": domains,
            "company_name": company_name
        })
        event_bus_name = "cyberscan-event-bus"
        entry = {
            'Time': datetime.datetime.now().isoformat(),
            'Source': source,
            'Resources': resources,
            'DetailType': detail_type,
            'Detail': detail,
            'EventBusName': event_bus_name
        }
        response = events.put_events(
            Entries=[
                entry
            ]
        )
        print(entry)
        print(response)

        table_name = "event_log"
        event_dqm_code = ''
        event_dqm_response = ''
        for entry in response["Entries"]:
            event_id = entry["EventId"]
            if "ErrorCode" in entry:
                error_code = entry["ErrorCode"]
            else:
                error_code = ""
            if "ErrorMessage" in entry:
                error_message = entry["ErrorMessage"]
            else:
                error_message = ""
            post_event_payload = {
                "consistencyLevel": "LOCAL_ONE",
                "ifNotExist": "false",
                "jsonClause": {
                    "EVENT_ID": event_id,
                    "TIMESTAMP": times,
                    "EVENT_ACTION": "PUBLISH",
                    "EVENT_ACTOR": str(source),
                    "RESOURCES": str(resources),
                    "DETAIL_TYPE": str(detail_type),
                    "DETAIL": str(detail),
                    "EVENT_BUS_NAME": str(event_bus_name),
                    "ERROR_CODE": str(error_code),
                    "ERROR_MESSAGE": str(error_message)
                },
                "timestamp": datetime.datetime.now().timestamp()
            }
            endpoint = f"api/clusters/{cluster_id}/keyspaces/{dqm_keyspace_id}/tables/{table_name}/insert"
            crud_url = f"{crud_api_url}/{endpoint}"
            event_dqm_response = requests.post(crud_url, data=json.dumps(post_event_payload), headers=headers)
            event_dqm_code = event_dqm_response.status_code
            event_dqm_response = event_dqm_response.content.decode("UTF-8")
            # event_dqm_response = json.dumps(event_dqm_response).replace("\"[", "[").replace("]\"", "]") \
            #     .replace("\'", "\"")
            print(event_dqm_code)
            print(event_dqm_response)


def get_scan_keys(url, scan_id):
    # does_scan_user_exist_json = {
    #     "allowFiltering": True,
    #     "consistencyLevel": "LOCAL_ONE",
    #     "distinct": True,
    #     "groupByClause": "SCAN_USER_ID",
    #     "limit": 1,
    #     "perPartitionLimit": 10,
    #     "selectClause": [
    #         "*"
    #     ],
    #     "whereClause": [
    #         "SCAN_ID = '" + scan_id + "'"
    #     ]
    # }
    does_scan_user_exist_json = {
        "allowFiltering": False,
        "consistencyLevel": "LOCAL_ONE",
        "distinct": True,
        "limit": 1,
        "perPartitionLimit": 10,
        "selectClause": [
            "*"
        ],
        "whereClause": [
            "SCAN_ID = '" + scan_id + "'"
        ]
    }
    response = requests.post(url, data=json.dumps(does_scan_user_exist_json), headers=headers)
    status_code = response.status_code
    body = json.loads(response.content.decode('utf-8'))
    # IF SCAN DOES NOT EXIST, RETURN 404 #
    if len(body) == 0:
        return "-1", "-1", "-1", "-1"
    else:
        print(body)
        body = body[0]
        body["domain"] = body["domain"].replace("\'", "\"")
        body = {k.upper(): v for k, v in body.items()}
        scan_user_id = body["SCAN_USER_ID"]
        company_name = body["COMPANY_NAME"]
        duns = body["DUNS"]
        domains = body["DOMAIN"]
        return scan_user_id, company_name, duns, domains


def store_meta_json(contents, url, user_id, s3_url):
    # STORE SCAN REQUEST IN WCAAS
    company_name = contents["name"]
    duns = contents["duns"]
    domains = contents["domains"]
    scan_id = contents["scan_id"]
    start_time = contents["start_time"]
    end_time = contents["end_time"]

    payload = {
        "consistencyLevel": "LOCAL_ONE",
        "ifNotExist": "false",
        "jsonClause": {
            "SCAN_ID": str(scan_id),
            "SCAN_USER_ID": user_id,
            "START_TIME": start_time.split(".")[0],
            "END_TIME": end_time.split(".")[0],
            "COMPANY_NAME": company_name,
            "DUNS": str(duns),
            "DOMAIN": str(domains),
            "S3_RAW_DUMP_URL": s3_url
        },
        "timestamp": datetime.datetime.now().timestamp()
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    status_code = response.status_code
    body = json.loads(response.content.decode('utf-8'))
    return status_code, body


def store_breach_json(contents, url, scan_id, scan_user_id, s3_url):
    # STORE SCAN REQUEST IN WCAAS
    status_code = ''
    body = {}
    for record in contents:
        email = record["email"]
        breach = record["breach_list"]

        payload = {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "SCAN_ID": str(scan_id),
                "SCAN_USER_ID": scan_user_id,
                "TIMESTAMP": datetime.datetime.now().isoformat(timespec='seconds'),
                "EMAIL": email,
                "BREACH_LIST": breach,
                "S3_RAW_DUMP_URL": s3_url
            },
            "timestamp": datetime.datetime.now().timestamp()
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        status_code = response.status_code
        body = json.loads(response.content.decode('utf-8'))

    return status_code, body


def store_dns_json(contents, url, scan_id, scan_user_id, s3_url):
    # STORE SCAN REQUEST IN WCAAS
    status_code = ''
    body = {}
    for entry in contents:
        if entry is not None:
            name = contents[entry]["name"]
            alookup = contents[entry]["alookup"]
            spf = contents[entry]["spf"]
            dmarc = contents[entry]["dmarc"]
            axfr = contents[entry]["axfr"]
            payload = {
                "consistencyLevel": "LOCAL_ONE",
                "ifNotExist": "false",
                "jsonClause": {
                    "SCAN_ID": str(scan_id),
                    "SCAN_USER_ID": str(scan_user_id),
                    "TIMESTAMP": datetime.datetime.now().isoformat(timespec='seconds'),
                    "DNS_RECORD_NAME": name,
                    "ALOOKUP_NAME": alookup["name"],
                    "ALOOKUP_STATUS": alookup["status"],
                    "ALOOKUP_TIMESTAMP": alookup["timestamp"].split("-")[0],
                    "ALOOKUP_DATA": alookup["data"],
                    "SPF_NAME": spf["name"],
                    "SPF_STATUS": spf["status"],
                    "SPF_TIMESTAMP": spf["timestamp"],
                    "SPF_DATA": spf["data"],
                    "DMARC_ALTERED_NAME": dmarc["altered_name"],
                    "DMARC_NAME": dmarc["name"],
                    "DMARC_STATUS": dmarc["status"],
                    "DMARC_TIMESTAMP": dmarc["timestamp"],
                    "DMARC_DATA": dmarc["data"],
                    "AXFR_ALLOWED": axfr["allowed"]
                },
                "timestamp": datetime.datetime.now().timestamp()
            }
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            status_code = response.status_code
            body = json.loads(response.content.decode('utf-8'))
    return status_code, body


def store_scan_json(contents, url, scan_id, scan_user_id, s3_url):
    # STORE SCAN REQUEST IN WCAAS
    status_code = ''
    body = {}
    base_url = url
    for ip_record in contents:
        print(ip_record)
        print(contents[ip_record])
        ip_protocol = contents[ip_record]["ip_protocol"]  # NUMERIC
        indicators = contents[ip_record]["indicators"]  # DICTIONARY
        for port in contents[ip_record]["ports"]:
            port_number = port
            port = contents[ip_record]["ports"][port]
            tls_validation = port["tls"]["validation"]["browser_trusted"]
            print(tls_validation)
            if bool(tls_validation):
                table_name = "scan_data_tls"
                url = url + table_name + "/insert"
                payload = {
                    "consistencyLevel": "LOCAL_ONE",
                    "ifNotExist": "false",
                    "jsonClause": {
                        "SCAN_ID": str(scan_id),
                        "SCAN_USER_ID": str(scan_user_id),
                        "TIMESTAMP": datetime.datetime.now().isoformat(timespec='seconds'),
                        "IP_ADDRESS": str(ip_record),
                        "PORT_NUMBER": str(port_number),
                        "IP_ADDRESS_PROTOCOL": str(ip_protocol),
                        "INDICATORS": str(indicators),
                        "PORT_PROTOCOL": str(get_port_protocol(port)),
                        "PORT_STATE": str(get_port_state(port)),
                        "PORT_NAME": str(get_port_name(port)),
                        "PORT_SERVICE_VERSION": str(get_port_service_version(port)),
                        "PORT_CPE": str(get_port_name(port)),
                        "TLS_VALIDATION_BROWSER_TRUSTED": "false",
                        "CSP_REPORT_PASS": str(get_csp_report_pass(port)),
                        "SET_COOKIE_REPORT_PASS": str(get_set_cookie_report_pass(port)),
                        "HSTS_REPORT_PASS": str(get_hsts_report_pass(port)),
                        "X_CONTENT_TYPE_REPORT_PASS": str(get_x_content_type_report_pass(port)),
                        "XSS_PROTECTION_REPORT_PASS": str(get_xss_protection_report_pass(port)),
                        "REPORT_PASS": "",
                        "REPORT_TOTAL": "",
                        "TLS_DATA": str(get_tls_data(port)),
                        # "TLS_CERT_VER": "", #str(get_tls_cert_ver(port)),
                        # "TLS_CERT_SER_NUM": "", #str(get_tls_cert_ser_num(port)),
                        # "TLS_SIG_ALG_NAME": "", #str(get_tls_sig_alg_name(port)),
                        # "TLS_SIG_ALG_OID": "", #str(get_tls_sig_alg_oid(port)),
                        # "TLS_ISSUER_NAME": "", #str(get_issuer_name(port)),
                        # "TLS_ISSUER_COUNTRY": "", #str(get_issuer_country(port)),
                        # "TLS_ISSUER_ORGANIZATION": "", #str(get_issuer_organization(port)),
                        # "TLS_ISSUER_DN": "", #str(get_issuer_dn(port)),
                        # "TLS_VALIDITY_START": "", #str(get_validity_start(port)),
                        # "TLS_VALIDITY_END": "", #str(get_validity_end(port)),
                        # "TLS_VALIDITY_LENGTH": "", #str(get_validity_length(port)),
                        # "TLS_SUBJECT_NAME": "", #str(get_subject_name(port)),
                        # "TLS_SUBJECT_COUNTRY": "", #str(get_subject_country(port)),
                        # "TLS_SUBJECT_LOCALITY": "", #str(get_subject_locality(port)),
                        # "TLS_SUBJECT_PROVINCE": "", #str(get_subject_province(port)),
                        # "TLS_SUBJECT_ORGANIZATION": "", #str(get_subject_organization(port)),
                        # "TLS_SUBJECT_ORGUNIT": "", #str(get_subject_org_unit(port)),
                        # "TLS_SUBJECT_DN": "", #str(get_subject_dn(port)),
                        # "TLS_SUBJECT_KEY_INFO_ALG": "", #str(get_subject_key_info_alg(port)),
                        # "TLS_SUBJECT_RSA_PUB_KEY_EXPONENT": "", #str(get_subject_rsa_pub_key_exponent(port)),
                        # "TLS_SUBJECT_RSA_PUB_KEY_MODULUS": "", #str(get_subject_rsa_pub_key_modulus(port)),
                        # "TLS_SUBJECT_RSA_PUB_KEY_LENGTH": "", #str(get_subject_rsa_pub_key_length(port)),
                        # "TLS_SUBJECT_SHA256_FINGERPRINT": "", #str(get_subject_sha256_fingerprint(port)),
                        # "TLS_EXTENSION_USAGE": "", #str(get_tls_extension_usage(port)),
                        # "TLS_BASIC_CONSTRAINTS": "", #str(get_basic_constraints(port)),
                        # "TLS_SUBJECT_ALT_NAME": "", #str(get_subject_alt_name(port)),
                        # "TLS_SUBJECT_CRL_DIST_POINTS": "", #str(get_subject_crl_dist_points(port)),
                        # "TLS_SUBJECT_AUTH_KEY_ID": "", #str(get_subject_auth_key_id(port)),
                        # "TLS_SUBJECT_SUBJ_KEY_ID": "", #str(get_subject_subj_key_id(port)),
                        # "TLS_EXTENDED_KEY_USAGE": "", #str(get_extended_key_usage(port)),
                        # "TLS_SIGNATURE_SIG_ALG_NAME": "", #str(get_signature_sig_alg_name(port)),
                        # "TLS_SIGNATURE_SIG_ALG_OID": "", #str(get_signature_sig_alg_oid(port)),
                        # "TLS_CERTIFICATE_POLICIES": "", #str(get_certificate_policies(port)),
                        # "TLS_AUTHORITY_INFO_ACCESS": "", #str(get_authority_info_access(port)),
                        # "TLS_SIGNED_CERTIFICATE_TIMESTAMPS": "", #str(get_signed_certificate_timestamps(port)),
                        # "TLS_SIGNATURE_VALUE": "", #str(get_signature_value(port)),
                        # "TLS_SIGNATURE_VALID": "", #str(get_signature_valid(port)),
                        # "TLS_SIGNATURE_SELF_SIGNED": "", #str(get_signature_self_signed(port)),
                        # "TLS_FINGERPRINT_MD5": "", #str(get_fingerprint_md5(port)),
                        # "TLS_FINGERPRINT_SHA1": "", #str(get_fingerprint_sha1(port)),
                        # "TLS_FINGERPRINT_SHA256": "", #str(get_fingerprint_sha256(port)),
                        # "TLS_TBS_NOCT_FINGERPRINT": "", #str(get_tbs_noct_fingerprint(port)),
                        # "TLS_SPKI_SUBJECT_FINGERPRINT": "", #str(get_spki_subject_fingerprint(port)),
                        # "TLS_TBS_FINGERPRINT": "",  #str(get_tbs_fingerprint(port)),
                        # "TLS_VALIDATION_LEVEL": "", #str(get_validation_level(port)),
                        # "TLS_NAMES": "", #str(get_names(port)),
                        # "TLS_REDACTED": "", #str(get_redacted(port)),
                        "S3_RAW_DUMP_URL": s3_url
                    },
                    "timestamp": datetime.datetime.now().timestamp()
                }
            else:
                table_name = "scan_data_http"
                url = url + table_name + "/insert"
                payload = {
                    "consistencyLevel": "LOCAL_ONE",
                    "ifNotExist": "false",
                    "jsonClause": {
                        "SCAN_ID": str(scan_id),
                        "SCAN_USER_ID": str(scan_user_id),
                        "TIMESTAMP": datetime.datetime.now().isoformat(timespec='seconds'),
                        "IP_ADDRESS": str(ip_record),
                        "PORT_NUMBER": str(port_number),
                        "IP_ADDRESS_PROTOCOL": str(ip_protocol),
                        "INDICATORS": str(indicators),
                        "PORT_PROTOCOL": str(get_port_protocol(port)),
                        "PORT_STATE": str(get_port_state(port)),
                        "PORT_NAME": str(get_port_name(port)),
                        "PORT_SERVICE_VERSION": str(get_port_service_version(port)),
                        "PORT_CPE": str(get_port_name(port)),
                        "TLS_VALIDATION_BROWSER_TRUSTED": "false",
                        "CSP_REPORT_PASS": str(get_csp_report_pass(port)),
                        "SET_COOKIE_REPORT_PASS": str(get_set_cookie_report_pass(port)),
                        "HSTS_REPORT_PASS": str(get_hsts_report_pass(port)),
                        "X_CONTENT_TYPE_REPORT_PASS": str(get_x_content_type_report_pass(port)),
                        "XSS_PROTECTION_REPORT_PASS": str(get_xss_protection_report_pass(port)),
                        "S3_RAW_DUMP_URL": s3_url
                    },
                    "timestamp": datetime.datetime.now().timestamp()
                }
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            status_code = response.status_code
            body = json.loads(response.content.decode('utf-8'))
            url = base_url
            print(status_code)
            print(body)
    return status_code, body


def get_port_protocol(port):
    if "protocol" in port:
        return port["protocol"]
    else:
        return ""


def get_port_state(port):
    if "state" in port:
        return port["state"]
    else:
        return ""


def get_port_name(port):
    if "name" in port:
        return port["name"]
    else:
        return ""


def get_port_service_version(port):
    if "service_version" in port:
        return port["service_version"]
    else:
        return ""


def get_port_cpe(port):
    if "cpe" in port:
        return port["cpe"]
    else:
        return ""


def get_csp_report_pass(port):
    if "headers" in port \
            and "report" in port["headers"] \
            and "csp_report" in port["headers"]["report"] \
            and "pass" in port["headers"]["report"]["csp_report"]:
        return port["headers"]["report"]["csp_report"]["pass"]
    else:
        return ""


def get_set_cookie_report_pass(port):
    if "headers" in port \
            and "report" in port["headers"] \
            and "set_cookie_report" in port["headers"]["report"] \
            and "pass" in port["headers"]["report"]["set_cookie_report"]:
        return port["headers"]["report"]["set_cookie_report"]["pass"]
    else:
        return ""


def get_hsts_report_pass(port):
    if "headers" in port \
            and "report" in port["headers"] \
            and "hsts_report" in port["headers"]["report"] \
            and "pass" in port["headers"]["report"]["hsts_report"]:
        return port["headers"]["report"]["hsts_report"]["pass"]
    else:
        return ""


def get_x_content_type_report_pass(port):
    if "headers" in port \
            and "report" in port["headers"] \
            and "x_content_type_report" in port["headers"]["report"] \
            and "pass" in port["headers"]["report"]["x_content_type_report"]:
        return port["headers"]["report"]["x_content_type_report"]["pass"]
    else:
        return ""


def get_tls_data(port):
    if "tls" in port:
        return port["tls"]
    else:
        return ""


def get_xss_protection_report_pass(port):
    if "headers" in port \
            and "report" in port["headers"] \
            and "xss_protection_report" in port["headers"]["report"] \
            and "pass" in port["headers"]["report"]["xss_protection_report"]:
        return port["headers"]["report"]["xss_protection_report"]["pass"]
    else:
        return ""


def get_tls_cert_ver(port):
    if "certificate" in port["tls"] \
            and "version" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["version"]
    else:
        return ""


def get_tls_cert_ser_num(port):
    if "certificate" in port["tls"] \
            and "serial_number" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["serial_number"]
    else:
        return ""


def get_tls_sig_alg_name(port):
    if "certificate" in port["tls"] \
            and "signature_algorithm" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["signature_algorithm"]["name"]
    else:
        return ""


def get_tls_sig_alg_oid(port):
    if "certificate" in port["tls"] \
            and "signature_algorithm" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["signature_algorithm"]["oid"]
    else:
        return ""


def get_issuer_name(port):
    if "certificate" in port["tls"] \
            and "issuer " in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["issuer"]["common_name"]
    else:
        return ""


def get_issuer_country(port):
    if "certificate" in port["tls"] \
            and "issuer" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["issuer"]["country"]
    else:
        return ""


def get_issuer_organization(port):
    if "certificate" in port["tls"] \
            and "issuer" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["issuer"]["organization"]
    else:
        return ""


def get_issuer_dn(port):
    if "certificate" in port["tls"] \
            and "issuer_dn" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["issuer_dn"]
    else:
        return ""


def get_validity_start(port):
    if "certificate" in port["tls"] \
            and "validity" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["validity"]["start"]
    else:
        return ""


def get_validity_end(port):
    if "certificate" in port["tls"] \
            and "validity" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["validity"]["end"]
    else:
        return ""


def get_validity_length(port):
    if "certificate" in port["tls"] \
            and "validity" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["validity"]["length"]
    else:
        return ""


def get_subject_name(port):
    if "certificate" in port["tls"] \
            and "subject" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject"]["common_name"]
    else:
        return ""


def get_subject_country(port):
    if "certificate" in port["tls"] \
            and "subject" in port["tls"]["certificate"] \
            and "country" in port["tls"]["certificate"]["subject"]:
        return port["tls"]["certificate"]["subject"]["country"]
    else:
        return ""


def get_subject_locality(port):
    if "certificate" in port["tls"] and "subject" in port["tls"]["certificate"] and "locality" in \
            port["tls"]["certificate"]["locality"]:
        return port["tls"]["certificate"]["subject"]["locality"]
    else:
        return ""


def get_subject_province(port):
    if "certificate" in port["tls"] and "subject" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject"]["province"]
    else:
        return ""


def get_subject_organization(port):
    if "certificate" in port["tls"] and "subject" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject"]["organization"]
    else:
        return ""


def get_subject_org_unit(port):
    if "certificate" in port["tls"] and "subject" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject"]["organizational_unit"]
    else:
        return ""


def get_subject_dn(port):
    if "certificate" in port["tls"] and "subject_dn" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject_dn"]
    else:
        return ""


def get_subject_key_info_alg(port):
    if "certificate" in port["tls"] and "subject_key_info" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject_key_info"]["key_algorithm"]["name"]
    else:
        return ""


def get_subject_rsa_pub_key_exponent(port):
    if "certificate" in port["tls"] and "subject_key_info" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject_key_info"]["rsa_public_key"]["exponent"]
    else:
        return ""


def get_subject_rsa_pub_key_modulus(port):
    if "certificate" in port["tls"] and "subject_key_info" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject_key_info"]["rsa_public_key"]["modulus"]
    else:
        return ""


def get_subject_rsa_pub_key_length(port):
    if "certificate" in port["tls"] and "subject_key_info" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject_key_info"]["rsa_public_key"]["length"]
    else:
        return ""


def get_subject_sha256_fingerprint(port):
    if "certificate" in port["tls"] and "subject_key_info" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["subject_key_info"]["fingerprint_sha256"]
    else:
        return ""


def get_tls_extension_usage(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["key_usage"]
    else:
        return ""


def get_basic_constraints(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["basic_constraints"]
    else:
        return ""


def get_subject_alt_name(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["subject_alt_name"]
    else:
        return ""


def get_subject_crl_dist_points(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["crl_distribution_points"]
    else:
        return ""


def get_subject_auth_key_id(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["authority_key_id"]
    else:
        return ""


def get_subject_subj_key_id(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["subject_key_id"]
    else:
        return ""


def get_extended_key_usage(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["extended_key_usage"]
    else:
        return ""


def get_signature_sig_alg_name(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["extended_key_usage"]
    else:
        return ""


def get_certificate_policies(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["certificate_policies"]
    else:
        return ""


def get_authority_info_access(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["authority_info_access"]
    else:
        return ""


def get_signed_certificate_timestamps(port):
    if "certificate" in port["tls"] and "extensions" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["extensions"]["signed_certificate_timestamps"]
    else:
        return ""


def get_signature_sig_alg_oid(port):
    if "certificate" in port["tls"] and "signature" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["signature"]["signature_algorithm"]["oid"]
    else:
        return ""


def get_signature_value(port):
    if "certificate" in port["tls"] and "signature" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["signature"]["value"]
    else:
        return ""


def get_signature_valid(port):
    if "certificate" in port["tls"] and "signature" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["signature"]["valid"]
    else:
        return ""


def get_signature_self_signed(port):
    if "certificate" in port["tls"] and "signature" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["signature"]["self-signed"]
    else:
        return ""


def get_fingerprint_md5(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["fingerprint_md5"]
    else:
        return ""


def get_fingerprint_sha1(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["fingerprint_sha1"]
    else:
        return ""


def get_fingerprint_sha256(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["fingerprint_sha256"]
    else:
        return ""


def get_tbs_noct_fingerprint(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["tbs_noct_fingerprint"]
    else:
        return ""


def get_spki_subject_fingerprint(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["spki_subject_fingerprint"]
    else:
        return ""


def get_tbs_fingerprint(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["tbs_fingerprint"]
    else:
        return ""


def get_validation_level(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["validation_level"]
    else:
        return ""


def get_names(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["names"]
    else:
        return ""


def get_redacted(port):
    if "certificate" in port["tls"] and "fingerprint_md5" in port["tls"]["certificate"]:
        return port["tls"]["certificate"]["redacted"]
    else:
        return ""
