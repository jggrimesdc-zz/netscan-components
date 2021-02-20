import boto3
import json
import os
import re
import uuid
from datetime import datetime
from urllib.parse import unquote, quote

import requests


class SecretUtils:
    """
    Defines high-level Secrets Management Utilities for Scan API lib functions.
    """

    @staticmethod
    def get_secret(secret_name: str, region: str) -> dict:
        """ Gets a secrete from AWS Secrets Manager

        :param secret_name:
            Name of the secret to get.
        :param region:
            Region the secret is stored.
        :return:
            JSON representation of the full response
        """
        session = boto3.session.Session()

        client = session.client(
            service_name='secretsmanager',
            region_name=region
        )

        response = client.get_secret_value(
            SecretId=secret_name
        )

        return response


class LoggingUtils:
    """
    Defines high-level Logging Utilities for Scan API lib functions.
    """

    @staticmethod
    def log_event(action: str, level: str, log: object):
        """ Logs to stdout.  When running on AWS Lambda, logs will appear in CloudWatch trails automatically.

        :param action:
            The action being taken by the application at this time.
        :param level:
            The level of severity or impact of said action.
        :param log:
            The information you are trying to log in this statement.
        """
        print(f"{action.upper()}::{level.upper()}::{log}")


class S3Utils:
    """
    Defines S3 utility methods for Scan API lib functions.
    """

    @staticmethod
    def get_file(bucket: str, key: str) -> dict:
        """ Gets a file from S3 using boto3.  Assumes all files are JSON encoded.

        :param bucket:
            The bucket to get the file from.
        :param key:
            The key of the object.
        :return:
            The JSON read from the file.
        """
        s3 = boto3.resource("s3")

        s3_file = s3.Object(bucket, key)
        json_content = json.loads(s3_file.get()["Body"].read().decode('utf-8'))
        if json_content is None:
            json_content = {}
        return json_content

    @staticmethod
    def get_file_list(bucket: str, key: str) -> list:
        """ Gets a file from S3 as a list using S3.

        :param bucket:
            The bucket to get the file from.
        :param key:
            The key of the object.
        :return:
            The JSON read from the file.
        """
        s3 = boto3.resource("s3")

        s3_file = s3.Object(bucket, key)
        file_list = s3_file.get()['Body'].read().decode('UTF-8').splitlines()
        if file_list is None:
            file_list = []
        return file_list

    @staticmethod
    def put_file(bucket: str, key: str, body: dict):
        """ Gets a file from S3 using boto3.  Assumes all files are JSON encoded.

        :param bucket:
            The bucket to get the file from.
        :param key:
            The key of the object.
        :param body:
            The file contents to save to S3.
        """
        client = boto3.client("s3")
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=str(body).encode("utf-8")
        )


class EventBridgeUtils:
    """
    Defines EventBridge utility methods for Scan API lib functions.
    """

    @staticmethod
    def get_event_log_payload(event: dict, timestamp: datetime) -> dict:
        """ Gets the meaningful payload values from an AWS EventBridge Event.

        :param event:
            An AWS EventBridge event.
        :param timestamp:
            The time to save the event at in WCaaS.
        :return:
            The WCaaS CRUD API Payload for persisting this event record.
        :raises:
            ScanException if the scan is missing one of the required fields.
            This exception should never be raised.
        """
        if "id" in event:
            event_id = event["id"]
        else:
            print("AWS EventBridge event does not contain an \"id\" field.  Please confirm schema has not changed.")
            raise ScanException
        if "resources" in event:
            event_resources = json.dumps(event["resources"])
        else:
            print(
                "AWS EventBridge event does not contain a \"resources\" field.  Please confirm schema has not changed.")
            raise ScanException
        if "detail-type" in event:
            event_detail_type = event["detail-type"]
        else:
            print(
                "AWS EventBridge event does not contain a \"detail-type\" field.  Please confirm schema has not "
                "changed.")
            raise ScanException
        if "detail" in event:
            event_detail = json.dumps(event["detail"])
        else:
            print("AWS EventBridge event does not contain a \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "EVENT_ID": event_id,
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "EVENT_ACTION": "CONSUME",
                "EVENT_ACTOR": "CYBERSCAN_SCORE_STATE_MACHINE",
                "RESOURCES": event_resources,
                "DETAIL_TYPE": event_detail_type,
                "DETAIL": event_detail,
                "EVENT_BUS_NAME": "cyberscan-event-bus",
                "ERROR_CODE": "",
                "ERROR_MESSAGE": ""
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def publish_dqm_event(event: dict) -> requests.Response:
        """ Publishes the content of an event to the DQM table.  This method should be called everytime a method is
        published or subscribed over EventBridge.

        :param event:
            The event to persist.
        :return:
            The requests.Response object from the WCaaS CRUD API.
        """
        event_log_table = "event_log"
        event_log_payload = EventBridgeUtils.get_event_log_payload(event, datetime.now())
        event_log_endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                             f"{EnvironmentSourcer.dqm_keyspace()}/tables/{event_log_table}/insert "
        return requests.post(f"{EnvironmentSourcer.crud_api_url()}/{event_log_endpoint}",
                             data=json.dumps(event_log_payload),
                             headers=RequestUtils.get_headers())


class SQSUtils:
    """
    Defines SQS utility methods for Scan API lib functions.
    """

    @staticmethod
    def poll_scan(aws_region: str, queue_name: str) -> dict:
        """
        Polls a scan that is ready for collection.
        :param queue_name:
        The queue to pull the messages from.
        :param aws_region:
        The region the queuing infrastructure is located in.
        :return:
        Returns the next message off the queue.
        """
        session = boto3.session.Session(region_name=aws_region)
        sqs_client = session.client("sqs")

        response = sqs_client.receive_message(
            QueueUrl=queue_name,
            AttributeNames=['All'],
            MessageAttributeNames=[
                'scan_id',
                'domains',
                'name',
                'duns'
            ],
            MaxNumberOfMessages=1,
            VisibilityTimeout=1,
            WaitTimeSeconds=3
        )
        if 'Messages' not in response.keys() or len(response['Messages']) == 0:
            return {}
        else:
            return response['Messages'][0]

    @staticmethod
    def delete_scan(aws_region: str, scan_submission_queue_url: str, receipt_handle: str) -> None:
        """
        Removes a scan from an SQS queue.

        :param scan_submission_queue_url:
        The queue URL you want to remove the message from.
        :param aws_region:
        The region the queue resides in.
        :param receipt_handle:
        The receipt handle to remove from the queue.
        :return:
        """
        session = boto3.session.Session(region_name=aws_region)
        sqs_client = session.client("sqs")
        sqs_client.delete_message(
            QueueUrl=scan_submission_queue_url,
            ReceiptHandle=receipt_handle
        )

    @staticmethod
    def publish_scan_to_sqs(aws_region: str, sqs_queue: str, scan_id: uuid.UUID, company_name: str, duns: str,
                            domains: list) -> dict:
        """
        Publishes a scan request to the SQS queue sourced from the environment.

        :param sqs_queue:
        The queue to publish the message to.
        :param aws_region:
        The region to publish to.
        :param scan_id:
        The scan_id to persist.
        :param company_name:
        The company_name to scan.
        :param duns:
        The duns of the target company.
        :param domains:
        The domains to scan.
        :return:
        The response from the SQS boto3 client.
        """
        session = boto3.session.Session(region_name=aws_region)
        sqs_client = session.client("sqs")

        sqs_response = sqs_client.send_message(
            QueueUrl=sqs_queue,
            MessageBody='new_scan_request',
            DelaySeconds=10,
            MessageAttributes={
                'scan_id': {
                    'StringValue': str(scan_id),
                    'DataType': 'String'
                },
                'name': {
                    'StringValue': company_name,
                    'DataType': 'String'
                },
                'duns': {
                    'StringValue': str(duns),
                    'DataType': 'String'
                },
                'domains': {
                    'StringValue': str(domains),
                    'DataType': 'String'
                }
            },
        )
        LoggingUtils.log_event("SQS_PUBLISH", "INFO", "Published SQS message " + sqs_response['MessageId'])
        return sqs_response

    @staticmethod
    def publish_failed_scan_message(aws_region: str, scan_id: uuid.UUID, request_count: int) -> dict:
        """
        Publishes a failed scan message to the dead letter queue.

        :param aws_region:
        The AWS region the queue resides in.
        :param scan_id:
        The scan ID that failed.
        :param request_count:
        The number of requests that scan attempted.
        :return:
        """
        session = boto3.session.Session(region_name=aws_region)
        sqs_client = session.client("sqs")

        sqs_response = sqs_client.send_message(
            QueueUrl=EnvironmentSourcer.scan_dead_letter_queue(),
            MessageBody=f'{scan_id} cannot be completed.',
            DelaySeconds=10,
            MessageAttributes={
                'scan_id': {
                    'StringValue': str(scan_id),
                    'DataType': 'String'
                },
                'request_count': {
                    'StringValue': str(request_count),
                    'DataType': 'String'
                }
            },
        )
        LoggingUtils.log_event("SQS_PUBLISH", "INFO", "Published SQS message " + sqs_response['MessageId'])
        return sqs_response


class WCaaSUtils:
    """
    API Functions that handle WCaaS operations.
    """

    @staticmethod
    def process_domains_for_wcaas_persistance(event_detail: dict) -> dict:
        """
        Processes domain data from string-serialized JSON input and converts it to a type that is understood by WCaaS.
        :param event_detail:
            The JSON data to extract domain information from.  Domain data should be at the top level of this dictionary
            under 'domains'.
        :return:
            A dictionary of domain data processed for WCaaS insertion.
        """
        domains = event_detail['domains']
        if type(domains) is list:
            domains = {domain.replace("%5B", "").replace("%5D", "").replace("%22", "").replace("%20", "") for domain in
                       domains}
        elif type(domains) is str:
            domains = {
                quote(domain).replace("%5B", "").replace("%5D", "").replace("%22", "").replace("%20", "")
                    .replace("%27", "") for domain in domains.split(",")
            }
        return domains

    @staticmethod
    def get_cassandra_pod_ips(cluster_name: str, cluster_id: str) -> list:
        """
        Returns the pod IPs of the underlying Cassandra cluster.
        :param cluster_name:
            The name of the cluster being accessed.  Used to determine the management API DNS address.
        :param cluster_id:
            The ID of the cluster being accessed.
        :return:
            The list of pod IP addresses.
        """
        mgmt_api_dns = WCaaSUtils.get_mgmt_api_dns(cluster_name)
        url = f"http://{mgmt_api_dns}:8080/api/clusters/{cluster_id}/connection"
        LoggingUtils.log_event("POD_IP_ENDPOINTS", "INFO", url)
        headers = {
            'x-netscan-customeraccountid': "wcaas-crud"
        }
        response = requests.get(url, headers=headers)

        ips = []
        if response.status_code > 299:
            LoggingUtils.log_event("MGMT_API_RESPONSE", "ERROR", response.content.decode('utf-8'))
        else:
            ips_with_ports = json.loads(response.text)['contactPointAddresses']
            ips = list(map(lambda ip: ip.split(':')[0], ips_with_ports))
        return ips

    @staticmethod
    def get_mgmt_api_dns(cluster_name: str) -> str:
        """
        Determines the DNS resolution name for the Management API.
        :param cluster_name:
            The cluster name of the WCaaS cluster.
        :return:
            The DNS resolved name of the ELB in front of the WCaaS Cluster.
        """
        client = boto3.client('elb', region_name='us-east-2')
        elb_response = client.describe_load_balancers()

        for elb in elb_response['LoadBalancerDescriptions']:
            tag_response = client.describe_tags(LoadBalancerNames=[elb['LoadBalancerName']])
            elb_tags = tag_response['TagDescriptions'][0]
            tags = elb_tags['Tags']

            is_correct_cluster = WCaaSUtils.has_tag_with_key_and_value(tags, f"kubernetes.io/cluster/{cluster_name}",
                                                                       "owned")
            is_mgmt_api = WCaaSUtils.has_tag_with_key_and_value(tags, "kubernetes.io/service-name",
                                                                f"wcaas-{cluster_name}/wcaas-mgmt-api")

            if is_correct_cluster and is_mgmt_api:
                return elb['DNSName']

        raise Exception("Management API Not Found")

    @staticmethod
    def has_tag_with_key_and_value(tags: dict, key: str, value: str) -> bool:
        """
        Determines of a tag is set to a specific value for a resource.
        :param tags:
            The list of tags.
        :param key:
            The target tag.
        :param value:
            The expected value.
        :return:
            True or False is the expected value is found or not.
        """
        for tag in tags:
            if tag['Key'] == key and tag['Value'] == value:
                return True
        return False

    @staticmethod
    def check_if_scan_is_submitted(scan_id: str) -> (bool, dict):
        """
        Checks in WCaaS if a scan has been submitted to the platform before.

        :param scan_id:
            The scan_id to search for.
        :return:
            True/False if the user is onboarded.
            Their representation in WCaaS if the scan has been submitted.
        """
        does_user_exist_json = {
            "allowFiltering": False,
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "false",
            "limit": 1,
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                "scan_id = '" + scan_id + "'"
            ]
        }
        table_name = "request_input"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}/" \
                   f"tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", does_user_exist_json)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(does_user_exist_json),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return False, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE_STATUS_CODE", "INFO", status_code)
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE_BODY", "INFO", body)
        if status_code == 200 and len(body) > 0:
            body = json.loads(body)
        if type(body) is list and len(body[0].keys()) > 0:
            body = RequestUtils.convert_dictionary_keys_to_lower(body[0])
            return True, body
        elif type(body) is dict and len(body.keys()) > 0:
            body = RequestUtils.convert_dictionary_keys_to_lower(body)
            return True, body
        else:
            return False, body

    @staticmethod
    def check_current_scan_count(scan_id: str) -> (bool, dict):
        """
        Checks in WCaaS how many times a scan has been attempted.

        :param scan_id:
        The Scan ID to search for.
        :return:
        True / False if we have a successful response from WCaaS.
        The Dictionary of response data needed for the application.
        """
        table_name = "request_count"
        does_user_exist_json = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "limit": 1,
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                "SCAN_ID = '" + scan_id + "'"
            ]
        }
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}/" \
                   f"tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", does_user_exist_json)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(does_user_exist_json),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return False, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE_STATUS_CODE", "INFO", status_code)
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE_BODY", "INFO", body)

        if len(body) > 0:
            body = json.loads(body)
        if status_code == 200 and type(body) is list:
            if len(body) < 1:
                body = {}
                return True, body
            elif len(body[0].keys()) > 0:
                body = RequestUtils.convert_dictionary_keys_to_lower(body[0])
                return True, body
        elif status_code == 200 and type(body) is dict and len(body.keys()) > 0:
            body = RequestUtils.convert_dictionary_keys_to_lower(body)
            return True, body
        else:
            return False, body

    @staticmethod
    def check_if_user_is_onboarded(netscan_customer_account_id: str, netscan_user_id: str) -> (bool, dict):
        """
        Checks in WCaaS if a user has been onboarded to the platform before.

        :param netscan_customer_account_id:
            The netscan_customer_account_id used to onboard.
        :param netscan_user_id:
            The netscan_user_id used to onboard.
        :return:
            True/False if the user is onboarded.
            Their representation in WCaaS if they are onboarded, including their scan_user_id.
        """
        # Allow filtering set to false, removed the status = onboarding since onboarding time is ordered asc.
        does_user_exist_json = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "false",
            "groupByClause": "CUSTOMER_ACCOUNT_ID, USER_ID",
            "limit": 1,
            "orderingByClause": "onboard_time ASC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                "CUSTOMER_ACCOUNT_ID = '" + netscan_customer_account_id + "'",
                "USER_ID = '" + netscan_user_id + "'"
            ]
        }
        table_name = "clients"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.mgmt_keyspace()}/" \
                   f"tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", does_user_exist_json)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(does_user_exist_json),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return False, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)
        body = json.loads(body)
        if status_code == 200 and len(body) > 0 and len(body[0].keys()) > 0:
            body = RequestUtils.convert_dictionary_keys_to_lower(body[0])
            body = RequestUtils.convert_timestamp_column_to_ISO8601(body, "onboard_time")
            return True, body
        else:
            return False, body

    @staticmethod
    def get_scan_meta_data(scan_id: str):
        table_name = "request_input"
        does_scan_exist = {
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
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}/" \
                   f"tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", does_scan_exist)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(does_scan_exist),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        body = response.content.decode('utf-8')
        if status_code > 499:
            return False, json.loads('[]')

        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE_STATUS_CODE", "INFO", status_code)
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE_BODY", "INFO", body)
        if status_code == 200 and len(body) > 0:
            body = json.loads(body)
        if type(body) is list and len(body) > 0 and len(body[0].keys()) > 0:
            body = RequestUtils.convert_dictionary_keys_to_lower(body[0])
            return True, body
        elif type(body) is dict and len(body.keys()) > 0:
            body = RequestUtils.convert_dictionary_keys_to_lower(body)
            return True, body
        else:
            return False, body

    @staticmethod
    def insert_new_scan_count(scan_id: str, count: int, timestamp: datetime) -> (int, dict):
        """
        Inserts a new scan counter for a scan ID.

        :param scan_id:
        The scan ID to update.
        :param count:
        The count to update the scan ID to.
        :param timestamp:
        The timestamp that the scan was updated to.
        :return:
        The status code and response object of the WCaaS response.
        """
        payload = {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "SCAN_ID": str(scan_id),
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "COUNT": count
            },
            "timestamp": timestamp.timestamp()
        }
        table_name = "request_count"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}" \
                   f"/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers())
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = json.loads(response.content.decode('utf-8'))
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE", "INFO", body)
        return status_code, body

    @staticmethod
    def insert_new_user_record(netscan_customer_account_id: str, netscan_user_id: str, user_id: str,
                               timestamp: datetime) -> (int, dict):
        """
        Inserts a new user, onboards, to WCaaS.

        :param netscan_customer_account_id:
            User's netscan_customer_account_id.
        :param netscan_user_id:
            User's netscan_user_id.
        :param user_id:
            User's user_id.
        :param timestamp:
            Timestamp at which the user was onboarded.
        :return:
            Status Code & Response object.
        """
        payload = {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "CUSTOMER_ACCOUNT_ID": netscan_customer_account_id,
                "USER_ID": netscan_user_id,
                "SCAN_USER_ID": user_id,
                "ONBOARD_TIME": timestamp.isoformat(timespec='seconds'),
                "STATUS": "onboarded"
            },
            "timestamp": timestamp.timestamp()
        }
        table_name = "clients"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.mgmt_keyspace()}" \
                   f"/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers())
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE", "INFO", body)
        body = json.loads(body)
        body = RequestUtils.convert_dictionary_keys_to_lower(body)
        body = RequestUtils.convert_timestamp_column_to_ISO8601(body, "onboard_time")
        return status_code, body

    @staticmethod
    def insert_scan_input_metadata(scan_id: uuid.UUID, user_id: uuid.UUID, company_name: str, duns: str, domains: list,
                                   timestamp: datetime) -> (int, dict):
        payload = {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "SCAN_ID": str(scan_id),
                "COMPANY_NAME": company_name,
                "DOMAIN": str(domains),
                "DUNS": str(duns),
                "SCAN_USER_ID": user_id
            },
            "timestamp": timestamp.timestamp()
        }
        table_name = "request_input"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}" \
                   f"/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers())
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads(json.dumps(response.content.decode('utf-8')))

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", status_code)
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", body)
        body = json.loads(body)
        body = RequestUtils.convert_dictionary_keys_to_lower(body)

        return status_code, body

    @staticmethod
    def insert_new_cached_scan_record(timestamp: datetime, scan_id: uuid.UUID, domains: list):
        cached_domains = str(domains).replace("\'", "\"")
        add_cached_scan_payload = {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "SCAN_ID": str(scan_id),
                "DOMAINS": cached_domains
            },
            "timestamp": timestamp.timestamp()
        }
        table_name = "cached_scans"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}" \
                   f"/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", add_cached_scan_payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(add_cached_scan_payload),
                                 headers=RequestUtils.get_headers())
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads(json.dumps(response.content.decode('utf-8')))

        body = response.content.decode('utf-8')
        return status_code, json.loads(body)

    @staticmethod
    def select_cached_scan(domains: list) -> (int, dict):
        """
        Queries WCaaS for a cached scan from the list of domains passed.
        :param domains:
        The list of domains that are cached in WCaaS.
        :return:
        The status code & body of the response from WCaaS.
        """
        cached_domains = str(domains).replace("\'", "\"")
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "false",
            "groupByClause": "timestamp",
            "limit": 100,
            "orderingByClause": "timestamp DESC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                f"domains = '{cached_domains}'"
            ]
        }
        table_name = "cached_scans"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.meta_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        if response.content is None or response.content.decode('utf-8') == "[]":
            return 204, {}

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        body = json.loads(body)[0]
        body = RequestUtils.convert_timestamp_column_to_ISO8601(body, "timestamp")
        body = RequestUtils.convert_dictionary_keys_to_lower(body)
        reduced_body = {
            "last_scan_date": body["timestamp"],
            "scan_id": body["scan_id"]
        }

        return status_code, reduced_body

    @staticmethod
    def select_dqm_records(event_actor: str, event_action: str) -> (int, dict):
        """
        Returns a selection of DQM events for replay based on the actor that acted, and the actions taken.
        :param event_actor:
            The actor that took the event.
        :param event_action:
            The action taken.
        :return:
            The status code of the request and the map of actions taken by the specified actor.
        """
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                f"event_actor = '{event_actor}'",
                f"event_action = '{event_action}'"
            ]
        }
        table_name = "event_log"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.dqm_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)
        body = json.loads(body)
        body = RequestUtils.convert_timestamp_column_to_ISO8601(body, "timestamp")
        body = RequestUtils.convert_dictionary_keys_to_lower(body)
        return status_code, body

    @staticmethod
    def get_status_by_scan_id_for_scan_user(scan_id: str, scan_user_id: str) -> (int, dict):
        """
        Gets the status of a scan by scan_id for a specific user.
        :param scan_id:
            The scan_id to retrieve.
        :param scan_user_id:
            The user that submitted the scan.
        :return:
            The status code and response from the WCaaS CRUD API.
        """
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        where_clause = f"scan_id = '{scan_id}' AND timestamp < '{timestamp}' AND scan_user_id = '{scan_user_id}'"
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "groupByClause": "timestamp",
            "limit": 100,
            "orderingByClause": "timestamp DESC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                where_clause
            ]
        }
        table_name = "by_scan_id"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.status_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        if body is None or body == "[]":
            status_code = 204

        body = json.loads(body)
        new_body = []
        for _, obj in enumerate(body):
            obj = RequestUtils.convert_timestamp_column_to_ISO8601(obj, "timestamp")
            obj = RequestUtils.convert_dictionary_keys_to_lower(obj)
            new_body.append(obj)
        body = new_body

        return status_code, body

    @staticmethod
    def get_status_by_company_name_for_scan_user(company_name: str, scan_user_id: str) -> (int, dict):
        """
        Gets the status of a scan by company_name for a specific user.
        :param company_name:
            The company_name to retrieve.
        :param scan_user_id:
            The user that submitted the scan.
        :return:
            The status code and response from the WCaaS CRUD API.
        """
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        where_clause = f"company_name = '{company_name}' AND timestamp < '{timestamp}' AND scan_user_id = '{scan_user_id}'"
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "groupByClause": "timestamp",
            "limit": 100,
            "orderingByClause": "timestamp DESC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                where_clause
            ]
        }
        table_name = "by_company_name"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.status_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        if body is None or body == "[]":
            status_code = 204

        body = json.loads(body)
        new_body = []
        for _, obj in enumerate(body):
            obj = RequestUtils.convert_timestamp_column_to_ISO8601(obj, "timestamp")
            obj = RequestUtils.convert_dictionary_keys_to_lower(obj)
            new_body.append(obj)
        body = new_body

        return status_code, body

    @staticmethod
    def get_status_by_domain_for_scan_user(domain: str, scan_user_id: str) -> (int, dict):
        """
        Gets the status of a scan by domain for a specific user.
        :param domain:
            The domain to retrieve.
        :param scan_user_id:
            The user that submitted the scan.
        :return:
            The status code and response from the WCaaS CRUD API.
        """
        table_name = "by_domain"
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        where_clause = f"domain_name = '{domain}' AND timestamp < '{timestamp}' AND scan_user_id = '{scan_user_id}'"
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "groupByClause": "timestamp",
            "limit": 100,
            "orderingByClause": "timestamp DESC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                where_clause
            ]
        }
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.status_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        if body is None or body == "[]":
            status_code = 204

        body = json.loads(body)
        new_body = []
        for _, obj in enumerate(body):
            obj = RequestUtils.convert_timestamp_column_to_ISO8601(obj, "timestamp")
            obj = RequestUtils.convert_dictionary_keys_to_lower(obj)
            new_body.append(obj)
        body = new_body

        return status_code, body

    @staticmethod
    def get_status_by_status_for_scan_user(status: str, scan_user_id: str) -> (int, dict):
        """
        Gets the status of a scan by scan_id for a specific user.
        :param status:
            The status to retrieve.
        :param scan_user_id:
            The user that submitted the scan.
        :return:
            The status code and response from the WCaaS CRUD API.
        """
        where_clause = f"scan_status = '{status}' AND scan_user_id = '{scan_user_id}'"
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "groupByClause": "timestamp",
            "limit": 100,
            "orderingByClause": "timestamp DESC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                where_clause
            ]
        }
        table_name = "by_scan_status"
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.status_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        if body is None or body == "[]":
            status_code = 204

        body = json.loads(body)
        new_body = []
        for _, obj in enumerate(body):
            obj = RequestUtils.convert_timestamp_column_to_ISO8601(obj, "timestamp")
            obj = RequestUtils.convert_dictionary_keys_to_lower(obj)
            new_body.append(obj)
        body = new_body

        return status_code, body

    @staticmethod
    def get_status_by_date_range_for_scan_user(start_date: str, end_date: str, scan_user_id: str) -> (int, dict):
        """
        Gets the status of a scan by date range for a specific user.
        :param start_date:
            The start_date to retrieve from.
        :param end_date:
            The end_date to retrieve to.
        :param scan_user_id:
            The user that submitted the scan.
        :return:
            The status code and response from the WCaaS CRUD API.
        """
        table_name = "by_date_range"
        where_clause = f"scan_start_time >= '{start_date}' AND scan_start_time <= '{end_date}' AND scan_user_id = " \
                       f"'{scan_user_id}' "
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "limit": 100,
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                where_clause
            ]
        }
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.status_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        if body is None or body == "[]":
            status_code = 204

        body = json.loads(body)
        new_body = []
        for _, obj in enumerate(body):
            obj = RequestUtils.convert_timestamp_column_to_ISO8601(obj, "scan_start_time")
            obj = RequestUtils.convert_dictionary_keys_to_lower(obj)
            new_body.append(obj)
        body = new_body

        return status_code, body

    @staticmethod
    def get_status_by_duns_for_scan_user(duns: int, scan_user_id: str) -> (int, dict):
        """
        Gets the status of a scan by duns for a specific user.
        :param duns:
            The duns to retrieve.
        :param scan_user_id:
            The user that submitted the scan.
        :return:
            The status code and response from the WCaaS CRUD API.
        """
        table_name = "by_duns"
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        where_clause = f"duns = '{duns}' AND timestamp < '{timestamp}' AND scan_user_id = '{scan_user_id}'"
        payload = {
            "allowFiltering": "false",
            "consistencyLevel": "LOCAL_ONE",
            "distinct": "true",
            "groupByClause": "timestamp",
            "limit": 100,
            "orderingByClause": "timestamp DESC",
            "perPartitionLimit": 10,
            "selectClause": [
                "*"
            ],
            "whereClause": [
                where_clause
            ]
        }
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/{EnvironmentSourcer.status_keyspace()}" \
                   f"/tables/{table_name}/select"
        LoggingUtils.log_event("QUERY_WCAAS_REQUEST", "INFO", payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}", data=json.dumps(payload),
                                 headers=RequestUtils.get_headers()
                                 )
        status_code = response.status_code
        if status_code > 499:
            return status_code, json.loads('[]')

        body = response.content.decode('utf-8')
        LoggingUtils.log_event("QUERY_WCAAS_RESPONSE", "INFO", body)

        if body is None or body == "[]":
            status_code = 204

        body = json.loads(body)
        new_body = []
        for _, obj in enumerate(body):
            obj = RequestUtils.convert_timestamp_column_to_ISO8601(obj, "timestamp")
            obj = RequestUtils.convert_dictionary_keys_to_lower(obj)
            new_body.append(obj)
        body = new_body

        return status_code, body


class RequestUtils:
    """
    API functions that handle Request operations.
    """

    @staticmethod
    def get_headers() -> dict:
        """ Gets CRUD API HTTP Headers.

        :return:
            A JSON Object containing the default headers required by all CRUD API interactions.
        """
        return {
            'X-netscan-CustomerAccountId': EnvironmentSourcer.tenant_id(),
            'X-netscan-UserId': "12345",
            'content-type': 'application/json;charset=UTF-8'
        }

    @staticmethod
    def __validate_incoming_headers_are_present(headers: dict) -> dict:
        """
        Tests if the headers passed contain the required headers.
        :param headers:
            The headers to check.
        :return:
            The list of invalid headers.
        """
        invalid_fields = {}
        if headers is None or headers is []:
            invalid_fields["x-netscan-customeraccountid"] = "Not Present"
            invalid_fields["x-netscan-userid"] = "Not Present"
        elif "x-netscan-customeraccountid" not in headers:
            invalid_fields["x-netscan-customeraccountid"] = "Not Present"
        elif "x-netscan-userid" not in headers:
            invalid_fields["x-netscan-userid"] = "Not Present"
        return invalid_fields

    @staticmethod
    def __validate_scan_submission_body_fields_are_present(body: dict) -> dict:
        """
        Tests if the body passed contain the required fields.
        :param body:
            The body to check.
        :return:
            The list of invalid body fields.
        """
        missing_fields = {}
        if "force" in body:
            force = body['force']
        else:
            force = False
        if type(force) is not bool:
            missing_fields["force"] = "force must be a boolean"
        if "domains" not in body:
            missing_fields["domains"] = "Not Present"
        if "company_name" not in body:
            missing_fields["company_name"] = "Not Present"
        if "duns" not in body:
            missing_fields["duns"] = "Not Found"
        return missing_fields

    @staticmethod
    def __validate_scan_submission_body_fields_are_valid(body: dict) -> dict:
        """
        Tests if the body passed adhere to netscan standards.
        :param body:
            The body to check.
        :return:
            The list of invalid body fields.
        """
        invalid_fields = {}
        company_name = body['company_name']
        domains = body['domains']
        domains.sort()
        duns = str(body['duns'])

        is_company_name_str = isinstance(company_name, str)
        domain_matcher = re.compile(r"(//|\s+|^)(\w\.|\w[A-Za-z0-9-]{0,61}\w\.){1,3}[A-Za-z]{2,6}")

        if not is_company_name_str:
            invalid_fields["company_name"] = company_name
        if not company_name:
            invalid_fields["company_name"] = company_name
        if type(domains) is list:
            for domain in domains:
                if not domain_matcher.match(domain):
                    invalid_fields["domains"] = domains
                    break
        else:
            invalid_fields["domains"] = domains
        if not duns.isdigit():
            invalid_fields["duns"] = duns

        return invalid_fields

    @staticmethod
    def __validate_incoming_headers_are_netscan_compliant(headers: dict) -> dict:
        """
        Tests if the headers passed adhere to netscan standards.
        :param headers:
            The headers to check.
        :return:
            The list of invalid headers.
        """
        invalid_fields = {}
        netscan_customer_account_id = str(headers["x-netscan-customeraccountid"]).strip()
        netscan_user_id = str(headers["x-netscan-userid"]).strip()
        user_id_matcher = re.compile("[a-v0-9]{2,20}")
        if not user_id_matcher.match(netscan_customer_account_id):
            invalid_fields["x-netscan-customeraccountid"] = netscan_customer_account_id
        elif not user_id_matcher.match(netscan_user_id):
            invalid_fields["x-netscan-userid"] = netscan_user_id
        return invalid_fields

    @staticmethod
    def validate_incoming_headers(headers: dict) -> (bool, dict):
        """
        Validates API request headers for presence and conformity to netscan standards.
        :param headers:
            The dictionary of headers passed in to the request.
        :return:
            True or False if the headers are valid.
            The dictionary of invalid headers.
        """
        missing_fields = RequestUtils.__validate_incoming_headers_are_present(headers)
        if len(missing_fields.keys()) > 0:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": missing_fields
            }
        invalid_fields = RequestUtils.__validate_incoming_headers_are_netscan_compliant(headers)
        if len(invalid_fields.keys()) > 0:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": invalid_fields
            }
        return True, {}

    @staticmethod
    def is_scan_forced(body: dict) -> bool:
        """
        Tests if the requested scan is submitted as a forced scan.
        :param body:
            The body to check.
        :return:
            True/False if the scan is forced or not.
        """
        if "force" in body:
            force = body['force']
        else:
            force = False
        return force

    @staticmethod
    def validate_incoming_scan_submission_body(body: dict) -> (bool, dict):
        """
        Validates API request bodies for presence and conformity to netscan standards.
        :param body:
            The dictionary of headers passed in to the request.
        :return:
            True or False if the body is valid.
            The dictionary of invalid body fields.
        """
        missing_fields = RequestUtils.__validate_scan_submission_body_fields_are_present(body)
        if len(missing_fields.keys()) > 0:
            return {
                "errorMessage": "Malformed Request",
                "errorDetails": missing_fields
            }
        missing_fields = RequestUtils.__validate_scan_submission_body_fields_are_valid(body)
        if len(missing_fields.keys()) > 0:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": missing_fields
            }
        return True, {}

    @staticmethod
    def validate_scanid_path_parameter(path_parameters: dict) -> (bool, dict):
        """
        Validates the Scan ID passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :return:
            True or False if the scan ID is present.
            The dictionary of path parameters that violate the conditions.
        """
        uuid_matcher = re.compile("[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}")
        if "scan_id" not in path_parameters:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"scan_id": "Not Found"}
            }
        if not uuid_matcher.match(path_parameters["scan_id"]):
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"scan_id": path_parameters["scan_id"]}
            }
        return True, {}

    @staticmethod
    def validate_domains_path_parameter(path_parameters: dict) -> (bool, dict):
        """
        Validates the Domains passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :return:
            True or False if the scan ID is present.
            The dictionary of path parameters that violate the conditions.
        """
        domain_matcher = re.compile(r"(//|\s+|^)(\w\.|\w[A-Za-z0-9-]{0,61}\w\.){1,3}[A-Za-z]{2,6}")
        if "domain" not in path_parameters:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"domain": "Not Found"}
            }
        domain = unquote(path_parameters["domain"])
        if not domain_matcher.match(path_parameters["domain"]):
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"domain": domain}
            }
        return True, {}

    @staticmethod
    def validate_daterange_path_parameter(path_parameters: dict) -> (bool, dict):
        """
        Validates the Date Range passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :return:
            True or False if the date range is present or improperly formatted.
            The dictionary of path parameters that violate the conditions.
        :raises
            Exception is raised if the date range passed cannot be parsed into python datetime objects.
        """
        date_range_matcher = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9]{2}:[0-9]{2}:[0-9]{2}) ?- ?([0-9]{4}-["
                                        r"0-9]{2}-[0-9]{2}[ T][0-9]{2}:[0-9]{2}:[0-9]{2})")
        if "date_range" not in path_parameters:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"date_range": "Not Found"}
            }
        date_range = str(unquote(path_parameters["date_range"])).strip()
        if not date_range_matcher.match(date_range):
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"date_range": path_parameters["scan_id"]}
            }
        try:
            date_range.replace("T", " ")
            start_date = datetime.strptime(date_range_matcher.match(date_range).group(1), "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(date_range_matcher.match(date_range).group(2), "%Y-%m-%d %H:%M:%S")
            if start_date > end_date:
                return False, {
                    "errorMessage": "Malformed Request",
                    "errorDetails": str(start_date) + " is greater than " + str(end_date)
                }
            else:
                return True, {
                    "start_date": start_date,
                    "end_date": end_date
                }
        except ValueError as err:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"ErrorBrief": "Could not parse date values.",
                                 "ErrorDetails": str(err)
                                 }
            }

    @staticmethod
    def validate_status_path_parameter(path_parameters: dict) -> (bool, dict):
        """
        Validates the status passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :return:
            True or False if the status is present.
            The dictionary of path parameters that violate the conditions.
        """
        if "status" not in path_parameters:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"status": "Not Found"}
            }
        if path_parameters["status"] not in ["queued", "collecting", "scoring", "retrying", "failed", "complete"]:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {"status": path_parameters["status"]}
            }
        return True, {}

    @staticmethod
    def validate_path_parameter(path_parameters: dict, target_key: str) -> (bool, dict):
        """
        Validates a general path parameter passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :param target_key:
            The path parameter to look for.
        :return:
            True or False if the target_key is present.
            The dictionary of path parameters that violate the conditions.
        """
        if target_key not in path_parameters:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {target_key: "Not Found"}
            }
        return True, {}

    @staticmethod
    def validate_digit_path_parameter(path_parameters: dict, target_key: str) -> (bool, dict):
        """
        Validates a numeric passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :param target_key:
            The path parameter to look for.
        :return:
            True or False if the target_key is present.
            The dictionary of path parameters that violate the conditions.
        """
        if target_key not in path_parameters:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {target_key: "Not Found"}
            }
        if not path_parameters[target_key].isdigit():
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": {target_key: path_parameters[target_key]}
            }
        return True, {}

    @staticmethod
    def validate_incoming_dqm_eventlog_request(path_parameters: dict) -> (bool, dict):
        """
        Validates the path parameters passed.

        :param path_parameters:
            The path parameters passed into this request.
        :return:
            True or False if the path parameters are valid.
            The dictionary of path parameters that violate the conditions.
        """
        missing_fields = RequestUtils.__validate_incoming_dqm_eventlog_parameters_exist(path_parameters)
        if len(missing_fields.keys()) > 0:
            return False, {
                "errorMessage": "Malformed Request",
                "errorDetails": missing_fields
            }
        return True, {}

    @staticmethod
    def __validate_incoming_dqm_eventlog_parameters_exist(path_parameters: dict) -> dict:
        """
        Validates the Scan ID passed in as a path parameter.

        :param path_parameters:
            The path parameters passed into this request.
        :return:
            True or False if the scan ID is present.
            The dictionary of path parameters that violate the conditions.
        """
        invalid_fields = {}
        if path_parameters is None or path_parameters is []:
            invalid_fields["event_actor"] = "Not Present"
            invalid_fields["ecvent_action"] = "Not Present"
        elif "event_actor" not in path_parameters:
            invalid_fields["event_actor"] = "Not Present"
        elif "event_action" not in path_parameters:
            invalid_fields["event_action"] = "Not Present"
        return invalid_fields

    @staticmethod
    def extract_netscan_headers(headers: dict) -> (str, str):
        """
        Returns the expected netscan headers.
        :param headers:
            The header dictionary to extract headers from.
        :return:
            The customer account id and user id needed to communicate with the CRUD API.
        """
        return str(headers["x-netscan-customeraccountid"]).strip(), str(headers["x-netscan-userid"]).strip()

    @staticmethod
    def extract_dqm_path_parameters(path_parameters: dict) -> (str, str):
        """
        Returns the expected path parameters for DQM namespace queries.
        :param path_parameters:
            The path parameters to extract the DQM parameters from.
        :return:
            The event actor and action to be extracted from the path parameters.
        """
        return str(unquote(path_parameters["event_actor"])).strip(), str(unquote(path_parameters["event_action"])) \
            .strip()

    @staticmethod
    def convert_timestamp_to_ISO8601(timestamp: str) -> str:
        """
        Converts a timestamp string to ISO8601 format.
        :param timestamp:
            The timestamp to convert.
        :return:
            The timestamp converted.
        """
        return timestamp.replace(" ", "T")

    @staticmethod
    def convert_timestamp_column_to_ISO8601(dictionary: dict, key: str) -> dict:
        """
        Converts a field in a dictionary to ISO8601 format.
        :param dictionary:
            The dictionary containing the field to convert.
        :param key:
            The key containing the timestamp to convert.
        :return:
            The dictionary with the converted timestamp.
        """
        new_timestamp = dictionary[key].replace(" ", "T")
        dictionary[key] = new_timestamp
        return dictionary

    @staticmethod
    def convert_dictionary_keys_to_lower(dictionary: dict) -> dict:
        """
        Converts the dictionary keys to a lower case.
        :param dictionary:
            The dictionary to convert to lower case.
        :return:
            The dictionary with lower case keys.
        """
        return {k.lower(): v for k, v in dictionary.items()}

    @staticmethod
    def return_api_call(status_code, body: str) -> dict:
        """
        Returns an AWS Lambda Proxy response object.
        :param status_code:
            The status code to return.
        :param body:
            The body to return.
        :return:
            The dictionary to return to API Gateway.
        """
        return {
            "isBase64Encoded": False,
            "statusCode": status_code,
            "headers": {},
            "multiValueHeaders": {},
            "body": body
        }

    @staticmethod
    def return_base64encoded_api_call(status_code, body: str) -> dict:
        """
        Returns an AWS Lambda Proxy response object with "application/json" headers and base64Encoded set to True.
        :param status_code:
            The status code to return.
        :param body:
            The body to return.
        :return:
            The dictionary to return to API Gateway.
        """
        return {
            "isBase64Encoded": True,
            "statusCode": status_code,
            "headers": {
                "content-type": "application/json"
            },
            "multiValueHeaders": {},
            "body": body
        }


class StatusChanger:
    """
    Methods that are used to craft status update commands for WCaaS.
    """

    @staticmethod
    def __get_update_status_by_scan_id_payload(event: dict, timestamp: datetime, status: str):
        """ Builds the HTTP Body for the CRUD API to update the status of a scan by scan id.

        :param event:
            The AWS EventBridge event that triggers this lambda function.
        :param timestamp:
            The timestamp to store this event record under in WCaaS.
        :param status:
            The status to update the scan record to in WCaaS.
        :return:
            The HTTP Body for the CRUD API to update the status of a scan.
        :raises:
            ScanException if the scan is missing a detail field.
            This exception should never be raised.
        """
        if "detail" in event:
            event_detail = event["detail"]
        else:
            print("AWS EventBridge event does not contain an \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "SCAN_ID": str(event_detail['scan_id']),
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "COMPANY_NAME": event_detail['company_name'],
                "SCAN_USER_ID": event_detail['scan_user_id'],
                "SCAN_STATUS": status,
                "DUNS": event_detail['duns']
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def __get_update_status_by_company_name(event: dict, timestamp: datetime, status: str):
        """ Builds the HTTP Body for the CRUD API to update the status of a scan by company name.

        :param event:
            The AWS EventBridge event that triggers this lambda function.
        :param timestamp:
            The timestamp to store this event record under in WCaaS.
        :param status:
            The status to update the scan record to in WCaaS.
        :return:
            The HTTP Body for the CRUD API to update the status of a scan.
        :raises:
            ScanException if the scan is missing a detail field.
            This exception should never be raised.
        """
        if "detail" in event:
            event_detail = event["detail"]
        else:
            print("AWS EventBridge event does not contain an \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "COMPANY_NAME": event_detail['company_name'],
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "SCAN_USER_ID": event_detail['scan_user_id'],
                "SCAN_ID": event_detail['scan_id'],
                "SCAN_STATUS": status,
                "DUNS": event_detail['duns']
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def __get_update_status_by_date_range(event: dict, timestamp: datetime, status: str):
        """ Builds the HTTP Body for the CRUD API to update the status of a scan by date range.

        :param event:
            The AWS EventBridge event that triggers this lambda function.
        :param timestamp:
            The timestamp to store this event record under in WCaaS.
        :param status:
            The status to update the scan record to in WCaaS.
        :return:
            The HTTP Body for the CRUD API to update the status of a scan.
        :raises:
            ScanException if the scan is missing a detail field.
            This exception should never be raised.
        """
        if "detail" in event:
            event_detail = event["detail"]
        else:
            print("AWS EventBridge event does not contain an \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "SCAN_START_TIME": timestamp.isoformat(timespec='seconds'),
                "SCAN_USER_ID": event_detail['scan_user_id'],
                "SCAN_ID": event_detail['scan_id'],
                "COMPANY_NAME": event_detail['company_name'],
                "SCAN_STATUS": status,
                "DUNS": event_detail['duns'],
                "DURATION": "-1"
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def __get_update_status_by_status(event: dict, timestamp: datetime, status: str):
        """ Builds the HTTP Body for the CRUD API to update the status of a scan by status.

        :param event:
            The AWS EventBridge event that triggers this lambda function.
        :param timestamp:
            The timestamp to store this event record under in WCaaS.
        :param status:
            The status to update the scan record to in WCaaS.
        :return:
            The HTTP Body for the CRUD API to update the status of a scan.
        :raises:
            ScanException if the scan is missing a detail field.
            This exception should never be raised.
        """
        if "detail" in event:
            event_detail = event["detail"]
        else:
            print("AWS EventBridge event does not contain an \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "SCAN_STATUS": status,
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "SCAN_USER_ID": event_detail['scan_user_id'],
                "SCAN_ID": event_detail['scan_id'],
                "COMPANY_NAME": event_detail['company_name'],
                "DUNS": event_detail['duns']
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def __get_update_status_by_domains(event: dict, domain: str, timestamp: datetime, status: str):
        """ Builds the HTTP Body for the CRUD API to update the status of a scan.

        :param event:
            The AWS EventBridge event that triggers this lambda function.
        :param domain:
            The domain to update in WCaaS.
        :param timestamp:
            The timestamp to store this event record under in WCaaS.
        :param status:
            The status to update the scan record to in WCaaS.
        :return:
            The HTTP Body for the CRUD API to update the status of a scan.
        :raises:
            ScanException if the scan is missing a detail field.
            This exception should never be raised.
        """
        if "detail" in event:
            event_detail = event["detail"]
        else:
            print("AWS EventBridge event does not contain an \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "DOMAIN_NAME": domain,
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "SCAN_USER_ID": event_detail['scan_user_id'],
                "SCAN_ID": event_detail['scan_id'],
                "COMPANY_NAME": event_detail['company_name'],
                "SCAN_STATUS": status,
                "DUNS": event_detail['duns']
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def __get_update_status_by_duns(event: dict, timestamp: datetime, status: str):
        """ Builds the HTTP Body for the CRUD API to update the status of a scan by DUNS.

            :param event:
                The AWS EventBridge event that triggers this lambda function.
            :param timestamp:
                The timestamp to store this event record under in WCaaS.
            :param status:
                The status to update the scan record to in WCaaS.
            :return:
                The HTTP Body for the CRUD API to update the status of a scan.
            :raises:
                ScanException if the scan is missing a detail field.
                This exception should never be raised.
            """
        if "detail" in event:
            event_detail = event["detail"]
        else:
            print("AWS EventBridge event does not contain an \"detail\" field.  Please confirm schema has not changed.")
            raise ScanException
        domains = WCaaSUtils.process_domains_for_wcaas_persistance(event_detail)
        return {
            "consistencyLevel": "LOCAL_ONE",
            "ifNotExist": "false",
            "jsonClause": {
                "DUNS": event_detail['duns'],
                "TIMESTAMP": timestamp.isoformat(timespec='seconds'),
                "SCAN_USER_ID": event_detail['scan_user_id'],
                "SCAN_ID": event_detail['scan_id'],
                "COMPANY_NAME": event_detail['company_name'],
                "DOMAIN_NAME": str(domains),
                "SCAN_STATUS": status
            },
            "timestamp": timestamp.timestamp()
        }

    @staticmethod
    def publish_status_by_scan_id(event: dict, status: str) -> requests.Response:
        """ Changes the status of a scan in the by_scan_id table to the specified scan status.

        :param event:
            The event containing the scan_id to be modified.
        :param status:
            The status to modify the specified event to.
        :return:
            The Requests.post Response object returned from the CRUD API.
        """
        table_name = "by_scan_id"
        update_status_payload = StatusChanger.__get_update_status_by_scan_id_payload(event, datetime.now(), status)
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                   f"{EnvironmentSourcer.status_keyspace()}/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", update_status_payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(update_status_payload),
                                 headers=RequestUtils.get_headers())
        response_status_code = response.status_code
        response_body = response.content.decode("utf-8")
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", response_status_code)
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", response_body)
        return response

    @staticmethod
    def publish_status_by_company_name(event: dict, status: str) -> requests.Response:
        """ Changes the status of a scan in the by_company_name table to the specified scan status.

        :param event:
            The event containing the scan_id to be modified.
        :param status:
            The status to modify the specified event to.
        :return:
            The Requests.post Response object returned from the CRUD API.
        """
        table_name = "by_company_name"
        update_status_payload = StatusChanger.__get_update_status_by_company_name(event, datetime.now(), status)
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                   f"{EnvironmentSourcer.status_keyspace()}/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", update_status_payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(update_status_payload),
                                 headers=RequestUtils.get_headers())
        response_status_code = response.status_code
        response_body = response.content.decode("utf-8")
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", response_status_code)
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", response_body)
        return response

    @staticmethod
    def publish_status_by_date_range(event: dict, status: str) -> requests.Response:
        """ Changes the status of a scan in the by_date_range table to the specified scan status.

        :param event:
            The event containing the scan_id to be modified.
        :param status:
            The status to modify the specified event to.
        :return:
            The Requests.post Response object returned from the CRUD API.
        """
        table_name = "by_date_range"
        update_status_payload = StatusChanger.__get_update_status_by_date_range(event, datetime.now(), status)
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                   f"{EnvironmentSourcer.status_keyspace()}/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", update_status_payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(update_status_payload),
                                 headers=RequestUtils.get_headers())
        response_status_code = response.status_code
        response_body = response.content.decode("utf-8")
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", response_status_code)
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", response_body)
        return response

    @staticmethod
    def publish_status_by_domains(event: dict, status: str) -> requests.Response:
        """ Changes the status of a scan in the by_domains table to the specified scan status.

        :param event:
            The event containing the scan_id to be modified.
        :param status:
            The status to modify the specified event to.
        :return:
            The Requests.post Response object returned from the CRUD API.  Returns the latest response from the CRUD API
            for multiple domains.  Returns an erroneous response for the first encountered Response with status code
            above 499.
        """
        table_name = "by_domain"
        domains = WCaaSUtils.process_domains_for_wcaas_persistance(json.loads(json.dumps(event['detail'])))
        internal_response = ""
        for domain in domains:
            update_status_payload = StatusChanger.__get_update_status_by_domains(event, domain, datetime.now(), status)
            endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                       f"{EnvironmentSourcer.status_keyspace()}/tables/{table_name}/insert"
            LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", update_status_payload)
            internal_response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                              data=json.dumps(update_status_payload),
                                              headers=RequestUtils.get_headers())
            temp_status = internal_response.status_code
            if temp_status > 499:
                return internal_response
            response_status_code = internal_response.status_code
            response_body = internal_response.content.decode("utf-8")
            LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", response_status_code)
            LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", response_body)
        return internal_response

    @staticmethod
    def publish_status_by_status(event: dict, status: str) -> requests.Response:
        """ Changes the status of a scan in the by_status table to the specified scan status.

        :param event:
            The event containing the scan_id to be modified.
        :param status:
            The status to modify the specified event to.
        :return:
            The Requests.post Response object returned from the CRUD API.
        """
        table_name = "by_scan_status"
        update_status_payload = StatusChanger.__get_update_status_by_status(event, datetime.now(), status)
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                   f"{EnvironmentSourcer.status_keyspace()}/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", update_status_payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(update_status_payload),
                                 headers=RequestUtils.get_headers())
        response_status_code = response.status_code
        response_body = response.content.decode("utf-8")
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", response_status_code)
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", response_body)
        return response

    @staticmethod
    def publish_status_by_duns(event: dict, status: str) -> requests.Response:
        """ Changes the status of a scan in the by_duns table to the specified scan status.

        :param event:
            The event containing the scan_id to be modified.
        :param status:
            The status to modify the specified event to.
        :return:
            The Requests.post Response object returned from the CRUD API.
        """
        table_name = "by_duns"
        update_status_payload = StatusChanger.__get_update_status_by_duns(event, datetime.now(), status)
        endpoint = f"api/clusters/{EnvironmentSourcer.cluster_id()}/keyspaces/" \
                   f"{EnvironmentSourcer.status_keyspace()}/tables/{table_name}/insert"
        LoggingUtils.log_event("INSERT_WCAAS_REQUEST", "INFO", update_status_payload)
        response = requests.post(f"{EnvironmentSourcer.crud_api_url()}/{endpoint}",
                                 data=json.dumps(update_status_payload),
                                 headers=RequestUtils.get_headers())
        response_status_code = response.status_code
        response_body = response.content.decode("utf-8")
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_STATUS_CODE", "INFO", response_status_code)
        LoggingUtils.log_event("INSERT_WCAAS_RESPONSE_BODY", "INFO", response_body)
        return response

    @staticmethod
    def publish_queued_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "queued".

        :param event:
            The event describing the scan to modify.
        """
        status = 'queued'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_scoring_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "scoring".

        :param event:
            The event describing the scan to modify.
        """
        status = 'scoring'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_serializing_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "serializing_results".

        :param event:
            The event describing the scan to modify.
        """
        status = 'serializing_results'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_failed_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "failed".

        :param event:
            The event describing the scan to modify.
        """
        status = 'failed'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_collecting_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "collecting".

        :param event:
            The event describing the scan to modify.
        """
        status = 'collecting'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_retrying_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "retrying".

        :param event:
            The event describing the scan to modify.
        """
        status = 'retrying'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_complete_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "scoring".

        :param event:
            The event describing the scan to modify.
        """
        status = 'complete'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)

    @staticmethod
    def publish_invaildated_status_updates(event: dict):
        """ Blanket status change for all relevant status tables.  Changes to "scoring".

        :param event:
            The event describing the scan to modify.
        """
        status = 'invalidated'
        StatusChanger.publish_status_by_scan_id(event, status)
        StatusChanger.publish_status_by_company_name(event, status)
        StatusChanger.publish_status_by_date_range(event, status)
        StatusChanger.publish_status_by_status(event, status)
        StatusChanger.publish_status_by_domains(event, status)
        StatusChanger.publish_status_by_duns(event, status)


class EnvironmentSourcer:
    """
    Defines the operating environment for this file.
    """

    @staticmethod
    def scan_dead_letter_queue() -> str:
        """
        DEAD LETTER QUEUE URL
        :return:
            Returns the environment variable for the Dead Letter Queue.
        """
        return os.environ.get("DEAD_LETTER_QUEUE_URL")

    @staticmethod
    def scan_submission_queue() -> str:
        """
        SCAN SUBMISSION QUEUE URL
        :return:
            Returns the environment variable for the Scan Submission Queue.
        """
        return os.environ.get("SCAN_SUBMISSION_QUEUE_URL")

    @staticmethod
    def crud_api_url() -> str:
        """
        CRUD API URL
        :return:
            Returns the environment variable for the WCaaS CRUD API URL.
        """
        return os.environ.get("CRUD_API_URL")

    @staticmethod
    def tenant_id() -> str:
        """
        TENANT ID
        :return:
            Returns the environment variable for the WCaaS Tenant ID.
        """
        return os.environ.get("WCAAS_SERVICE_TENANT_ID")

    @staticmethod
    def cluster_id() -> str:
        """
        CLUSTER ID
        :return:
            Returns the environment variable for the WCaaS Cluster ID.
        """
        return os.environ.get("WCAAS_SERVICE_CLUSTER_ID")

    @staticmethod
    def dqm_keyspace() -> str:
        """
        DQM KEYSPACE
        :return:
            Returns the environment variable for the dqm keyspace.
        """
        return os.environ.get("DQM_KEYSPACE")

    @staticmethod
    def meta_keyspace() -> str:
        """
        META KEYSPACE
        :return:
            Returns the environment variable for the meta keyspace.
        """
        return os.environ.get("META_DATA_KEYSPACE")

    @staticmethod
    def score_keyspace() -> str:
        """
        SCORE KEYSPACE
        :return:
            Returns the environment variable for the score keyspace.
        """
        return os.environ.get("SCORE_KEYSPACE")

    @staticmethod
    def status_keyspace() -> str:
        """
        STATUS KEYSPACE
        :return:
            Returns the environment variable for the status keyspace.
        """
        return os.environ.get("STATUS_KEYSPACE")

    @staticmethod
    def mgmt_keyspace() -> str:
        """
        MGMT KEYSPACE
        :return:
            Returns the environment variable for the management keyspace.
        """
        return os.environ.get("MGMT_KEYSPACE")

    @staticmethod
    def retry_count() -> int:
        """
        RETRY LIMIT
        :return:
            Returns the environment variable for scan retry limit, with a default value of 3 retries.
        """
        return int(os.environ.get("RETRY_LIMIT", 3))


##############
# EXCEPTIONS #
##############
class ScanException(Exception):
    pass
