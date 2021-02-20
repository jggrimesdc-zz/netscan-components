import boto3
import json
import os
import pytest
import requests
import unittest
from collections import namedtuple
from datetime import datetime
from moto import mock_elb, mock_secretsmanager, mock_s3
from unittest import mock

from layers.python.scan_api_lib import EnvironmentSourcer as ENV
from layers.python.scan_api_lib import EventBridgeUtils
from layers.python.scan_api_lib import RequestUtils as REQ
from layers.python.scan_api_lib import S3Utils
from layers.python.scan_api_lib import SecretUtils
from layers.python.scan_api_lib import WCaaSUtils as WCAAS, WCaaSUtils
from test import scan_test_properties as test_values

""" Dummy client for boto3 """


class DummyClient(object):
    """
    A Dummy Client. All attributes/methods redirect to the `DummyClient.do_nothing` method, which
    ignores all arguments except a single keyword argument: `return_value`. If `return_value` is

    # Create a dummy client:
    # >>> from resources.dummy_boto3_client import DummyClient
    # >>> client = DummyClient('s3')

    # Call a method the client would have:
    # >>> client.upload_file('tmp/file_name.txt', 'some-bucket', 'data/file_name.txt')
    {'statusCode': 200}

    # With a return value:
    # >>> client.list_buckets(return_value=['bucket-a','bucket-b'])
    ['bucket-a', 'bucket-b']
    """
    default_return_value = {
        'statusCode': 200
    }

    def __init__(self, client_name, *args, **kwargs):
        self.client_name = client_name

    def do_nothing(self, *args, return_value=None, return_none=False, **kwargs):
        """
        Does nothing, then returns:
            - `None` if `return_none` is True,
            - `return_value` if `return_value` is not None
            - `DummyClient.return_value` if neither `return_none` or `return_value` are set

        To change the default return value, you can change the `default_return_value` property on
        a client instance:

        # >>> client = DummyClient('lambda')
        # >>> client.default_return_value = True
        # >>> client.invoke_function('a')
        True
        """

        if return_none:
            return None
        elif return_value is not None:
            return return_value
        return self.default_return_value

    def __getattr__(self, attr):
        """ Overrides attribute finder to always return `DummyClient.do_nothing` """
        if attr == '__str__':
            return str(self)
        if attr == '__repr__':
            return repr(self)
        return self.do_nothing

    def __str__(self):
        return f"Dummy boto3 {self.client_type} client."

    def __repr__(self):
        return f"DummyClient({self.client_type})"


##############
# UNIT TESTS #
##############
class UnitTestEnvironmentSourcer(unittest.TestCase):

    @mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
    def test_get_crud_api_url(self):
        self.assertEqual(os.environ.get("CRUD_API_URL"), ENV.crud_api_url())

    @mock.patch.dict(os.environ, {"WCAAS_SERVICE_TENANT_ID": test_values.TENANT_ID})
    def test_get_tenant_id(self):
        self.assertEqual(os.environ.get("WCAAS_SERVICE_TENANT_ID"), ENV.tenant_id())

    @mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
    def test_get_cluster_id(self):
        self.assertEqual(os.environ.get("WCAAS_SERVICE_CLUSTER_ID"), ENV.cluster_id())

    @mock.patch.dict(os.environ, {"DQM_KEYSPACE": test_values.DQM_KEYSPACE})
    def test_get_dqm_keyspace(self):
        self.assertEqual(os.environ.get("DQM_KEYSPACE"), ENV.dqm_keyspace())

    @mock.patch.dict(os.environ, {"SCORE_KEYSPACE": test_values.SCORE_KEYSPACE})
    def test_get_score_keyspace(self):
        self.assertEqual(os.environ.get("SCORE_KEYSPACE"), ENV.score_keyspace())

    @mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
    def test_get_status_keyspace(self):
        self.assertEqual(os.environ.get("STATUS_KEYSPACE"), ENV.status_keyspace())


class UnitTestRequestUtils(unittest.TestCase):

    @mock.patch.dict(os.environ, {"WCAAS_SERVICE_TENANT_ID": test_values.TENANT_ID})
    def test_get_headers(self):
        headers = {
            'X-netscan-CustomerAccountId': os.environ.get("WCAAS_SERVICE_TENANT_ID"),
            'X-netscan-UserId': "12345",
            'content-type': 'application/json;charset=UTF-8'
        }
        self.assertEqual(headers, REQ.get_headers())


class UnitTestWCaaSUtils(unittest.TestCase):

    def test_process_domains_for_wcaas_persistance(self):
        list_domains_test = {
            "scan_id": "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29",
            "company_name": "Test Company",
            "scan_user_id": "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29",
            "duns": "12345",
            "domains": ["testdomain1.com", "testdomain2.com"]
        }
        string_domains_test = {
            "scan_id": "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29",
            "company_name": "Test Company",
            "scan_user_id": "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29",
            "duns": "12345",
            "domains": "['testdomain1.com', 'testdomain2.com']"
        }
        list_domains_result = WCAAS.process_domains_for_wcaas_persistance(list_domains_test)
        string_domains_result = WCAAS.process_domains_for_wcaas_persistance(string_domains_test)
        self.assertEqual(list_domains_result, string_domains_result)

    @mock_elb
    def test_get_mgmt_api_dns(self):
        client = boto3.client('elb', region_name='us-east-2')
        test_cluster_name = "test_wcaas_cluster"

        # CREATE WHAT I EXPECT TO SEE
        client.create_load_balancer(LoadBalancerName="TestLB",
                                    Listeners=[
                                        {
                                            'Protocol': 'HTTP',
                                            'LoadBalancerPort': 80,
                                            'InstanceProtocol': 'HTTP',
                                            'InstancePort': 80
                                        },
                                    ],
                                    Tags=[
                                        {
                                            'Key': f'kubernetes.io/cluster/{test_cluster_name}',
                                            'Value': 'owned'
                                        }, {
                                            'Key': 'kubernetes.io/service-name',
                                            'Value': f'wcaas-{test_cluster_name}/wcaas-mgmt-api'
                                        }
                                    ])
        dns_name = WCaaSUtils.get_mgmt_api_dns(test_cluster_name)
        self.assertTrue(dns_name is not None)

    @mock_elb
    def test_get_mgmt_api_dns_exception(self):
        with pytest.raises(Exception) as e_info:
            WCaaSUtils.get_mgmt_api_dns("test_wcaas_cluster")
        self.assertTrue(e_info.value.args[0] == 'Management API Not Found')

    def test_tag_with_key_and_value_missing(self):
        self.assertFalse(WCaaSUtils.has_tag_with_key_and_value({}, "testKey", "testVal"))


###################
# COMPONENT TESTS #
###################
# region check_if_user_is_onboarded
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"MGMT_KEYSPACE": test_values.MGMT_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['mgmt_user_status_event_normal'])
def test_search_for_onboarded_user_exists(events, event_name, monkeypatch):
    """
    This test checks the mgmt_client_onboard_status_handler.py and corresponding library functions.

    This test checks the appropriate output for a user that exists in WCaaS.

    :param events:
        Library of events to be referenced.
    :param event_name:
        Name of the event under test.
    :param monkeypatch:
        Patching tool used to hijack API calls.
    :return:
        * Assert true that WCaaS confirms user has onboarded successfully.
        * Assert that WCaaS JSON-Stringified response is the same as the JSON-Stringified expected response.
        * Assert that Lambda JSON response object is the same as the JSON expected response object.
    """
    test_status_code = 200
    event = events[event_name]['event']
    customer_account_id, user_id = REQ.extract_netscan_headers(event["headers"])
    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))
    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response

    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_onboarded, response = WCAAS.check_if_user_is_onboarded(customer_account_id, user_id)

    assert is_onboarded
    assert (response == json.loads(dummy_response.content.decode('utf-8'))[0])


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"MGMT_KEYSPACE": test_values.MGMT_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['mgmt_user_status_event_normal'])
def test_search_for_onboarded_user_not_exists(events, event_name, monkeypatch):
    """
    This test checks the mgmt_client_onboard_status_handler.py and corresponding library functions.

    This test checks the appropriate output for a user that does not exist in WCaaS.

    :param events:
        Library of events to be referenced.
    :param event_name:
        Name of the event under test.
    :param monkeypatch:
        Patching tool used to hijack API calls.
    :return:
        * Assert true that WCaaS confirms user has onboarded successfully.
        * Assert that WCaaS JSON-Stringified response is the same as the JSON-Stringified expected response.
        * Assert that Lambda JSON response object is the same as the JSON expected response object.
    """
    test_status_code = 200
    event = events[event_name]['event']
    customer_account_id, user_id = REQ.extract_netscan_headers(event["headers"])
    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_not_found'])
                                   .encode(encoding='UTF-8'))
    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response

    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_onboarded, response = WCAAS.check_if_user_is_onboarded(customer_account_id, user_id)

    assert not is_onboarded
    assert (response == json.loads(dummy_response.content.decode('utf-8')))


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"MGMT_KEYSPACE": test_values.MGMT_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['mgmt_user_status_event_normal'])
def test_search_for_onboarded_user_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    event = events[event_name]['event']
    customer_account_id, user_id = REQ.extract_netscan_headers(event["headers"])
    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_not_found'])
                                   .encode(encoding='UTF-8'))
    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response

    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_onboarded, response = WCAAS.check_if_user_is_onboarded(customer_account_id, user_id)

    assert not is_onboarded
    assert (response == [])


# endregion

# region insert_new_user_record
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['mgmt_user_onboard_event_normal'])
def test_insert_new_user_count_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    event = events[event_name]['event']
    customer_account_id, netscan_user_id = REQ.extract_netscan_headers(event["headers"])
    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_new_user_record(customer_account_id, netscan_user_id, test_user_id,
                                                         test_onboard_time)
    assert status_code == test_status_code
    assert response == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"MGMT_KEYSPACE": test_values.MGMT_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['mgmt_user_onboard_event_normal'])
def test_onboard_new_user_normal(events, event_name, monkeypatch):
    """
    This test checks the mgmt_client_onboard_handler.py and corresponding library functions.

    This test checks if a lambda function allows for the proper onboarding of a new user.

    :param events:
        Library of events to be referenced.
    :param event_name:
        Name of the event under test.
    :param monkeypatch:
        Patching tool used to hijack API calls.
    :return:
        * Assert true that WCaaS confirms user has not been onboarded before.
        * Assert that WCaaS JSON-Stringified response is the same as the JSON-Stringified expected response.
        * Assert that Lambda JSON response object is the same as the JSON expected response object.
    """
    test_status_code = 201
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    event = events[event_name]['event']
    customer_account_id, netscan_user_id = REQ.extract_netscan_headers(event["headers"])
    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_new_user_record(customer_account_id, netscan_user_id, test_user_id,
                                                         test_onboard_time)
    assert status_code == test_status_code
    assert (json.dumps(response) == json.dumps(json.loads(dummy_response.content.decode('utf-8'))))


# endregion

# region insert_new_scan_count
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['insert_new_scan_count'])
def test_insert_new_scan_count(events, event_name, monkeypatch):
    test_status_code = 201
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_new_scan_count(test_scan_id, 1, test_onboard_time)
    assert status_code == test_status_code
    assert response == events[event_name]['expected_response_normal']


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['insert_new_scan_count'])
def test_insert_new_scan_count_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_new_scan_count(test_scan_id, 1, test_onboard_time)
    assert status_code == test_status_code
    assert response == []


# endregion

# region insert_scan_input_meta_data
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['insert_new_scan_count'])
def test_insert_scan_input_meta_data(events, event_name, monkeypatch):
    test_status_code = 201
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_scan_input_metadata(test_scan_id, test_user_id, "", "", [], test_onboard_time)
    assert status_code == test_status_code
    assert response == events[event_name]['expected_response_normal']


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['insert_new_scan_count'])
def test_insert_scan_input_meta_data_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_scan_input_metadata(test_scan_id, test_user_id, "", "", [], test_onboard_time)
    assert status_code == test_status_code
    assert response is not None


# endregion

# region insert_new_cached_scan_record
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['insert_new_scan_count'])
def test_insert_new_cached_scan_record(events, event_name, monkeypatch):
    test_status_code = 201
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_new_cached_scan_record(test_onboard_time, test_scan_id, [])
    assert status_code == test_status_code
    assert response['scan_user_id'] == events[event_name]['expected_response_normal']['scan_user_id']


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['insert_new_scan_count'])
def test_insert_new_cached_scan_record_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_onboard_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['expected_response_normal'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, response = WCAAS.insert_new_cached_scan_record(test_onboard_time, test_scan_id, [])
    assert status_code == test_status_code
    assert response is not None


# endregion

# region check_if_scan_is_submitted tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_if_scan_submitted'])
def test_check_if_scan_is_submitted(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['submitted_scan'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_if_scan_is_submitted(test_scan_id)
    assert is_submitted
    assert body['scan_id'] == test_scan_id
    assert body['scan_user_id'] == test_user_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_if_scan_submitted'])
def test_check_if_scan_is_submitted_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['submitted_scan'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_if_scan_is_submitted(test_scan_id)
    assert not is_submitted
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_if_scan_submitted'])
def test_check_if_scan_is_submitted_list_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['submitted_scan_list_response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_if_scan_is_submitted(test_scan_id)
    assert is_submitted
    assert body['scan_id'] == test_scan_id
    assert body['scan_user_id'] == test_user_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_if_scan_submitted'])
def test_check_if_scan_is_submitted_string_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['submitted_scan_string_response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_if_scan_is_submitted(test_scan_id)
    assert not is_submitted
    assert body == events[event_name]['submitted_scan_string_response']


# endregion

# region check_cached_scan tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_cached_scan'])
def test_select_cached_scan(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_domains = []

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.select_cached_scan(test_domains)
    assert status_code == test_status_code
    assert body['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_cached_scan'])
def test_select_cached_scan_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_domains = []

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.select_cached_scan(test_scan_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_cached_scan'])
def test_select_cached_scan_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_domains = []

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content="[]"
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.select_cached_scan(test_scan_id)
    assert status_code == test_status_code
    assert body == {}


# endregion

# region check_dqm_records tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"DQM_KEYSPACE": test_values.DQM_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['dqm_events'])
def test_select_dqm_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_domains = []

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.select_dqm_records("actor", "action")
    assert status_code == test_status_code
    assert body['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"DQM_KEYSPACE": test_values.DQM_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['dqm_events'])
def test_select_dqm_records_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.select_dqm_records("actor", "action")
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_status_by_scan_id tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_scan_id_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_scan_id_for_scan_user(test_scan_id, test_user_id)
    assert status_code == test_status_code
    assert body[0]['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_scan_id_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_scan_id_for_scan_user(test_scan_id, test_user_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_scan_id_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=str("[]")
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_scan_id_for_scan_user(test_scan_id, test_user_id)
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_status_by_company_name tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_company_name_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_company_name_for_scan_user("Google", test_user_id)
    assert status_code == test_status_code
    assert body[0]['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_company_name_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_company_name_for_scan_user("Google", test_user_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_company_name_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=str("[]")
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_company_name_for_scan_user("Google", test_user_id)
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_status_by_domain tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_domain_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_domain_for_scan_user("google.com", test_user_id)
    assert status_code == test_status_code
    assert body[0]['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_domain_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_domain_for_scan_user("google.com", test_user_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_domain_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=str("[]")
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_domain_for_scan_user("google.com", test_user_id)
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_status_by_status tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_status_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_status_for_scan_user("complete", test_user_id)
    assert status_code == test_status_code
    assert body[0]['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_status_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_status_for_scan_user("complete", test_user_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_status_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=str("[]")
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_status_for_scan_user("complete", test_user_id)
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_status_by_duns tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_duns_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_duns_for_scan_user(12345, test_user_id)
    assert status_code == test_status_code
    assert body[0]['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_duns_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_duns_for_scan_user(12345, test_user_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_duns_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=str("[]")
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_duns_for_scan_user(12345, test_user_id)
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_status_by_date_range tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_date_range_records(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_start_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")
    test_end_time = datetime.strptime("2020-09-08T12:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['date_response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_date_range_for_scan_user(test_start_time, test_end_time, test_user_id)
    assert status_code == test_status_code
    assert body[0]['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_date_range_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_start_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")
    test_end_time = datetime.strptime("2020-09-08T12:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['date_response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_date_range_for_scan_user(test_start_time, test_end_time, test_user_id)
    assert status_code == test_status_code
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"STATUS_KEYSPACE": test_values.STATUS_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['status_events'])
def test_status_by_date_range_empty_response(events, event_name, monkeypatch):
    test_status_code = 204
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"
    test_start_time = datetime.strptime("2020-09-08T11:30:17", "%Y-%m-%dT%H:%M:%S")
    test_end_time = datetime.strptime("2020-09-08T12:30:17", "%Y-%m-%dT%H:%M:%S")

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=str("[]")
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    status_code, body = WCaaSUtils.get_status_by_date_range_for_scan_user(test_start_time, test_end_time, test_user_id)
    assert status_code == test_status_code
    assert body == []


# endregion

# region check_current_scan_count tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_scan_count'])
def test_check_current_scan_count(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_current_scan_count(test_scan_id)
    assert is_submitted
    assert body['scan_id'] == test_scan_id
    assert body['scan_user_id'] == test_user_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_scan_count'])
def test_check_current_scan_count_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_current_scan_count(test_scan_id)
    assert not is_submitted
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_scan_count'])
def test_check_current_scan_count_non200_response(events, event_name, monkeypatch):
    test_status_code = 300
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_current_scan_count(test_scan_id)
    assert not is_submitted
    assert body['scan_id'] == test_scan_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_scan_count'])
def test_check_current_scan_count_empty_list_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response_list_empty'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_current_scan_count(test_scan_id)
    assert is_submitted
    assert body == {}


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_check_scan_count'])
def test_check_current_scan_count_list_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response_list'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.check_current_scan_count(test_scan_id)
    assert is_submitted
    assert body == events[event_name]['response_list'][0]


# endregion

# region get_scan_meta_data tests
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_scan_meta_data'])
def test_get_scan_meta_data(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.get_scan_meta_data(test_scan_id)
    assert is_submitted
    assert body['scan_id'] == test_scan_id
    assert body['scan_user_id'] == test_user_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_scan_meta_data'])
def test_get_scan_meta_data_500_response(events, event_name, monkeypatch):
    test_status_code = 500
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.get_scan_meta_data(test_scan_id)
    assert not is_submitted
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_scan_meta_data'])
def test_get_scan_meta_data_list_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"
    test_user_id = "d4163a7b-66b5-4597-89bc-370ac5b5c993"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response_list'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.get_scan_meta_data(test_scan_id)
    assert is_submitted
    assert body['scan_id'] == test_scan_id
    assert body['scan_user_id'] == test_user_id


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_scan_meta_data'])
def test_get_scan_meta_data_empty_list_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['response_list_empty'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.get_scan_meta_data(test_scan_id)
    assert not is_submitted
    assert body == []


@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"META_KEYSPACE": test_values.META_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
@pytest.mark.parametrize('event_name', ['scan_get_scan_meta_data'])
def test_get_scan_meta_data_string_response(events, event_name, monkeypatch):
    test_status_code = 200
    test_scan_id = "12a3d2e9-049e-4d4f-bfc4-49e2a69bef29"

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=test_status_code,
                                   content=json.dumps(events[event_name]['submitted_scan_string_response'])
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    is_submitted, body = WCaaSUtils.get_scan_meta_data(test_scan_id)
    assert not is_submitted
    assert body == events[event_name]['submitted_scan_string_response']


# endregion

# region get_cassandra_pod_ips tests
@mock_elb
@pytest.mark.parametrize('event_name', ['mgmt_get_cassandra_pod_ips'])
def test_get_cassandra_pod_ips(events, event_name, monkeypatch):
    client = boto3.client('elb', region_name='us-east-2')
    test_cluster_name = "test_wcaas_cluster"
    test_cluster_id = "12345"

    # CREATE WHAT I EXPECT TO SEE
    client.create_load_balancer(LoadBalancerName="TestLB",
                                Listeners=[
                                    {
                                        'Protocol': 'HTTP',
                                        'LoadBalancerPort': 80,
                                        'InstanceProtocol': 'HTTP',
                                        'InstancePort': 80
                                    },
                                ],
                                Tags=[
                                    {
                                        'Key': f'kubernetes.io/cluster/{test_cluster_name}',
                                        'Value': 'owned'
                                    }, {
                                        'Key': 'kubernetes.io/service-name',
                                        'Value': f'wcaas-{test_cluster_name}/wcaas-mgmt-api'
                                    }
                                ])

    DummyResponse = namedtuple('Response', ['status_code', 'text'])
    dummy_response = DummyResponse(status_code=200,
                                   text=json.dumps(events[event_name]['event']).encode(encoding='UTF-8'))
    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'get', dummy_requests.get)

    ips = WCaaSUtils.get_cassandra_pod_ips(test_cluster_name, test_cluster_id)
    assert ("127.0.0.1" in ips)
    assert ("196.0.0.1" in ips)


@mock_elb
@pytest.mark.parametrize('event_name', ['mgmt_get_cassandra_pod_ips'])
def test_get_cassandra_pod_ips_error_response(events, event_name, monkeypatch):
    client = boto3.client('elb', region_name='us-east-2')
    test_cluster_name = "test_wcaas_cluster"
    test_cluster_id = "12345"

    # CREATE WHAT I EXPECT TO SEE
    client.create_load_balancer(LoadBalancerName="TestLB",
                                Listeners=[
                                    {
                                        'Protocol': 'HTTP',
                                        'LoadBalancerPort': 80,
                                        'InstanceProtocol': 'HTTP',
                                        'InstancePort': 80
                                    },
                                ],
                                Tags=[
                                    {
                                        'Key': f'kubernetes.io/cluster/{test_cluster_name}',
                                        'Value': 'owned'
                                    }, {
                                        'Key': 'kubernetes.io/service-name',
                                        'Value': f'wcaas-{test_cluster_name}/wcaas-mgmt-api'
                                    }
                                ])

    DummyResponse = namedtuple('Response', ['status_code', 'content', 'text'])
    dummy_response = DummyResponse(status_code=300,
                                   content=json.dumps(events[event_name]['event']).encode(encoding='UTF-8'),
                                   text=json.dumps(events[event_name]['event']).encode(encoding='UTF-8'))
    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'get', dummy_requests.get)

    ips = WCaaSUtils.get_cassandra_pod_ips(test_cluster_name, test_cluster_id)
    assert (len(ips) == 0)


# endregion

# region test_secrets_utils
@mock_secretsmanager
def test_get_secret():
    client = boto3.client("secretsmanager", region_name="us-east-2")
    client.put_secret_value(SecretId="test_secret", SecretString="secret_value")

    response = SecretUtils.get_secret("test_secret", "us-east-2")
    assert response["SecretString"] == "secret_value"


# endregion

# region test_s3_utils
@mock_s3
def test_get_file():
    conn = boto3.resource('s3', region_name='us-east-2')
    conn.create_bucket(Bucket='test_bucket')

    s3 = boto3.client('s3', region_name='us-east-2')
    s3.put_object(Bucket='test_bucket', Key='test_key', Body=str("{}").encode("utf-8"))

    file_content = S3Utils.get_file("test_bucket", "test_key")
    assert file_content == {}


@mock_s3
def test_put_file():
    conn = boto3.resource('s3', region_name='us-east-2')
    conn.create_bucket(Bucket='test_bucket')

    S3Utils.put_file("test_bucket", "test_key", {})

    body = conn.Object('test_bucket', 'test_key').get()['Body'].read().decode("utf-8")

    assert body == '{}'


# endregion

# region test_event_bridge_utils
@mock.patch.dict(os.environ, {"CRUD_API_URL": test_values.CRUD_API_URL})
@mock.patch.dict(os.environ, {"DQM_KEYSPACE": test_values.DQM_KEYSPACE})
@mock.patch.dict(os.environ, {"WCAAS_SERVICE_CLUSTER_ID": test_values.CLUSTER_ID})
def test_publish_dqm_event(monkeypatch):
    test_event = {
        "id": "event_value",
        "resources": [],
        "detail-type": "detailed information",
        "detail": "less detail"
    }

    DummyResponse = namedtuple('Response', ['status_code', 'content'])
    dummy_response = DummyResponse(status_code=200,
                                   content=json.dumps({})
                                   .encode(encoding='UTF-8'))

    dummy_requests = DummyClient('requests')
    dummy_requests.default_return_value = dummy_response
    monkeypatch.setattr(requests, 'post', dummy_requests.post)

    response = EventBridgeUtils.publish_dqm_event(test_event)

    assert response.status_code == 200


# endregion

env_suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestEnvironmentSourcer)
req_suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestRequestUtils)
unittest.TextTestRunner(verbosity=2).run(env_suite)
unittest.TextTestRunner(verbosity=2).run(req_suite)
