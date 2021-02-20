import os
import pandas as pd
import time
from datetime import date

from base_worker import BaseWorker


class IngestBlackarch(BaseWorker):
    '''
    Class specifically for the cloning and ingesting blackarch data from github 
    '''

    def __init__(self, source, label, file, config, df=None):
        self.file = file
        self.url = self.file['url']
        self.source = source
        self.label = label
        self.bucket = config.bucket
        self.s3_client = config.s3_client
        self.prefix = 'raw'
        self.df = pd.DataFrame()

    def clone_blackarch(self):
        # clone the blackarch repo
        os.system(f"git clone {self.url} /tmp/blackarch")

        # printing time for testing purposes
        print("git clone at " + time.strftime("%H:%M:%S", time.localtime()))

        # traverse blackarch repo
        path = '/tmp/blackarch/packages'
        # path = '/Users/johngrimes/Downloads/blackarch/packages'
        # dirs = os.listdir(path)

        # write data to s3
        raw_s3_path = f"{self.prefix}/{self.source}/{self.label}-{date.today()}"

        # write raw data to s3
        for root, d_names, f_names in os.walk(path):
            if root != path:
                package_name = root.split('/')[-1]

                for source_file in f_names:
                    s3_object_key = f"{raw_s3_path}/{package_name}/{source_file}"
                    print(f"{path}/{package_name}/{source_file}")

                    response = self.s3_client.upload_file(f"{path}/{package_name}/{source_file}", self.bucket,
                                                          s3_object_key)

    def run_all(self):
        self.clone_blackarch()
