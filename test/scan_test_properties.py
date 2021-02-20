CRUD_API_URL = "http://internal-a671d9171b3ea4d52b0416326d746dfb-1552705679.us-east-2.elb.amazonaws.com:8080"
TENANT_ID = "wcaas-stable-crud"
CLUSTER_ID = "20401"
DQM_KEYSPACE = "dqm"
META_KEYSPACE = "meta "
MGMT_KEYSPACE = "mgmt"
SCAN_KEYSPACE = "scan"
SCORE_KEYSPACE = "score"
STATUS_KEYSPACE = "status"

SCORING_PIPELINE_START_EVENT_NORMAL = {
    "version": "0",
    "id": "46e9c0c9-96f8-bda0-0743-d62849d71451",
    "detail-type": "Trigger Downstream Analytics",
    "source": "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER",
    "account": "500841576861",
    "time": "2020-08-20T13:37:48Z",
    "region": "us-east-2",
    "resources": [
        "CyberScan Collectors",
        "S3",
        "Lambda:ScanSerializer"
    ],
    "detail": {
        "bucket_name": "cyber-scan-qa",
        "scan_id": "4aa874ad-9be8-4411-a261-ddc2ff826542",
        "scan_user_id": "7c8c4247-f1ea-479e-895e-0e2bac65033e",
        "duns": "00012345",
        "domains": [
            "netscan.com"
        ],
        "company_name": "SmokeTest"
    }
}
SCORING_PIPELINE_START_EVENT_MISSING_ID = {
    "version": "0",
    "detail-type": "Trigger Downstream Analytics",
    "source": "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER",
    "account": "500841576861",
    "time": "2020-08-20T13:37:48Z",
    "region": "us-east-2",
    "resources": [
        "CyberScan Collectors",
        "S3",
        "Lambda:ScanSerializer"
    ],
    "detail": {
        "bucket_name": "cyber-scan-qa",
        "scan_id": "4aa874ad-9be8-4411-a261-ddc2ff826542",
        "scan_user_id": "7c8c4247-f1ea-479e-895e-0e2bac65033e",
        "duns": "00012345",
        "domains": [
            "netscan.com"
        ],
        "company_name": "SmokeTest"
    }
}
SCORING_PIPELINE_START_EVENT_MISSING_RESOURCES = {
    "version": "0",
    "id": "46e9c0c9-96f8-bda0-0743-d62849d71451",
    "detail-type": "Trigger Downstream Analytics",
    "source": "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER",
    "account": "500841576861",
    "time": "2020-08-20T13:37:48Z",
    "region": "us-east-2",
    "detail": {
        "bucket_name": "cyber-scan-qa",
        "scan_id": "4aa874ad-9be8-4411-a261-ddc2ff826542",
        "scan_user_id": "7c8c4247-f1ea-479e-895e-0e2bac65033e",
        "duns": "00012345",
        "domains": [
            "netscan.com"
        ],
        "company_name": "SmokeTest"
    }
}
SCORING_PIPELINE_START_EVENT_MISSING_DETAIL_TYPE = {
    "version": "0",
    "id": "46e9c0c9-96f8-bda0-0743-d62849d71451",
    "source": "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER",
    "account": "500841576861",
    "time": "2020-08-20T13:37:48Z",
    "region": "us-east-2",
    "resources": [
        "CyberScan Collectors",
        "S3",
        "Lambda:ScanSerializer"
    ],
    "detail": {
        "bucket_name": "cyber-scan-qa",
        "scan_id": "4aa874ad-9be8-4411-a261-ddc2ff826542",
        "scan_user_id": "7c8c4247-f1ea-479e-895e-0e2bac65033e",
        "duns": "00012345",
        "domains": [
            "netscan.com"
        ],
        "company_name": "SmokeTest"
    }
}
SCORING_PIPELINE_START_EVENT_MISSING_DETAIL = {
    "version": "0",
    "id": "46e9c0c9-96f8-bda0-0743-d62849d71451",
    "detail-type": "Trigger Downstream Analytics",
    "source": "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER",
    "account": "500841576861",
    "time": "2020-08-20T13:37:48Z",
    "region": "us-east-2",
    "resources": [
        "CyberScan Collectors",
        "S3",
        "Lambda:ScanSerializer"
    ]
}
