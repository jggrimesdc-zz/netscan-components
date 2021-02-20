def main(event, context):
    # TODO: Retrieve src results and store them in WCaaS

    # response = requests.get("CyberScanApi/api/v1/src/report/{scan_id}")

    # POC usage: print event contents

    return {
        'statusCode': 200,
        'body': event
    }
