import json
import pandas as pd
from datetime import date

from base_worker import BaseWorker


class ReadJSONNested(BaseWorker):
    """
    Class to read json files that need to be normalized. Currently used for
    Vulnerability sources (previously `read_json_vuln`
    """

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
        self.json_key = self.file.get("json_key")
        self.id_col_rev = self.file.get('id_col_rev')
        self.id_col_raw = self.file.get("id_col_raw")

    def get_json_file_from_s3(self):
        raw_json = json.loads(self.obj.get()['Body'].read().decode('utf-8'))

        if self.json_key is not None:
            self.df = pd.json_normalize(raw_json[self.json_key])
        else:
            self.df = pd.json_normalize(raw_json)

        if self.id_col_raw is not None and self.id_col_rev is not None:
            self.df[self.id_col_rev] = self.df[self.id_col_raw].str[:8]

    def run_all(self):
        self.get_json_file_from_s3()
        return self.df
