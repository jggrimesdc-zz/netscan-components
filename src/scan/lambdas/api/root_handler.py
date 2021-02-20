from __future__ import print_function

from scan_api_lib import RequestUtils

print('Loading function')


def handle(event, context):
    return RequestUtils.return_api_call(200, "{}")
