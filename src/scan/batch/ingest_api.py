import json
import requests
from datetime import date

from base_worker import BaseWorker


class IngestFilesAPI(BaseWorker):

    def __init__(self, source, label, file, config, df=None):
        self.config = config
        self.source = source
        self.label = label
        self.file = file
        self.bucket = self.config.bucket
        self.s3_client = self.config.s3_client
        self.prefix = "raw"
        self.json_key = self.file['json_key']

    def save_files(self):
        body = requests.get(self.file['url']).json()[self.json_key]
        body_json = bytes(json.dumps(body).encode('UTF-8'))
        self.s3_client.put_object(
            Body=body_json,
            Bucket=self.bucket,
            Key=f"{self.prefix}/{self.source}/{self.label}/{self.label}-{date.today()}{self.file['file_type']}"
        )

    def run_all(self):
        self.save_files()
