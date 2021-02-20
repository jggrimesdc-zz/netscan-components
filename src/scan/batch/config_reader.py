import boto3
import json
import os


class GetConfig:
    '''
    Reads in config file. Bucket needs to be specified in AWS Batch job definition as environmental variable "BUCKET".
    '''

    def __init__(self):
        self.bucket = os.getenv('BUCKET')
        self.breach_source_bucket = os.getenv('BREACH_SOURCE_BUCKET')
        self.key = 'config/config.json'
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.config_file = self.s3_client.get_object(Bucket=self.bucket,
                                                     Key=self.key)
        self.config_json = json.loads(self.config_file['Body'].read().decode('utf-8'))
