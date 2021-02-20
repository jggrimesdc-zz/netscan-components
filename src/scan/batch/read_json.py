import json
import pandas as pd
from datetime import date

from base_worker import BaseWorker


class ReadJSON(BaseWorker):

    def __init__(self, source, label, file, config, df=None):
        self.source = source
        self.label = label
        self.file = file
        self.s3_client = config.s3_client
        self.s3_resource = config.s3_resource
        self.bucket = config.bucket
        self.file_type = self.file['file_type']
        self.key = f"raw/{self.source}/{self.label}/{self.label}-{date.today()}{self.file_type}"
        self.obj = self.s3_resource.Object(bucket_name=self.bucket,
                                           key=self.key)
        self.today = date.today().strftime('%Y-%m-%d')
        self.df = pd.DataFrame()
        self.json_key = self.file['json_key']

    def get_json_file_from_s3(self):
        json_file = json.loads(self.obj.get()['Body'].read().decode('utf-8'))
        self.df = pd.DataFrame(json_file)

    def run_all(self):
        self.get_json_file_from_s3()
        return self.df
