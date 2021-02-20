import pandas as pd
from datetime import date

from base_worker import BaseWorker


class ReadCSV(BaseWorker):
    '''
    A simple csv reader for files where the columns are correctly specified in the original document. 
    '''

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
        self.df = pd.DataFrame()

    def get_file_from_s3(self):
        self.df = pd.read_csv(self.obj.get()['Body'])

    def run_all(self):
        self.get_file_from_s3()
        return self.df
