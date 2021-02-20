from __future__ import print_function

print('Loading function')


def handle(event, context):
    return {
        "statusCode": 505,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "Query by Company ID not supported."
    }
