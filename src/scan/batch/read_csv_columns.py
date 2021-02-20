import pandas as pd
import time
from datetime import date

from base_worker import BaseWorker


class ReadCSVColumns(BaseWorker):
    '''
    A csv reader for large files where the columns are not included in the source file 
    '''

    def __init__(self, source, label, file, config, df=None):
        self.source = source
        self.label = label
        self.file = file
        self.s3_resource = config.s3_resource
        self.bucket = config.bucket
        self.file_type = self.file['file_type']
        self.key = f"raw/{self.source}/{self.label}/{self.label}-{date.today()}{self.file_type}"
        self.obj = self.s3_resource.Object(bucket_name=self.bucket,
                                           key=self.key)
        self.df = pd.DataFrame()
        self.columns = self.file['columns']
        self.dtypes = self.file['dtypes']
        self.date = self.file['date_col']
        self.df_list = []

    def get_file_from_s3(self):
        csv_chunks = pd.read_csv(self.obj.get()['Body'],
                                 names=self.columns,
                                 dtype=self.dtypes,
                                 parse_dates=self.date,
                                 chunksize=10000)
        for chunk in csv_chunks:
            self.df_list.append(chunk)
            print(len(self.df_list))
        print("chunking completed at " + time.strftime("%H:%M:%S", time.localtime()))

        self.df = pd.concat(self.df_list)
        print("df concat'd at " + time.strftime("%H:%M:%S", time.localtime()))

    def run_all(self):
        self.get_file_from_s3()
        return self.df
