import boto3
import datetime
import fastparquet as fp
import json
import pandas as pd
import s3fs
import time
import uuid

from base_worker import BaseWorker


class ReadBreachJL(BaseWorker):
    '''
    Class specifically for the breach jl files (json list) 
    '''

    def __init__(self, source, label, file, config, df=None):
        self.source = source
        self.label = label
        self.file = file
        self.s3_client = config.s3_client
        self.s3_resource = config.s3_resource
        self.bucket = config.breach_source_bucket
        self.file_type = self.file['file_type']
        self.key = f"{self.label}"
        self.obj = self.s3_resource.Object(bucket_name=self.bucket,
                                           key=self.key)
        self.df = pd.DataFrame()

    def get_breach_file_from_s3(self):
        # breach_json = df = pd.read_json(self.obj.get()['Body'].read().decode('utf-8'),lines=True) #json.loads(self.obj.get()['Body'].read().decode('utf-8'))
        # self.df = breach_json #pd.json_normalize(breach_json)

        # adding in chunking due to memory constraints
        df_list = []
        breach_json = pd.read_json(self.obj.get()['Body'].read().decode('utf-8'),
                                   lines=True, chunksize=1000)
        for chunk in breach_json:
            df_list.append(chunk)

        # printing time for testing purposes
        print("chunking completed at " + time.strftime("%H:%M:%S", time.localtime()))

        self.df = pd.concat(df_list)
        print("df concat'd at " + time.strftime("%H:%M:%S", time.localtime()))
        print(self.df.info())

    def run_all(self):
        self.get_breach_file_from_s3()
        return self.df
