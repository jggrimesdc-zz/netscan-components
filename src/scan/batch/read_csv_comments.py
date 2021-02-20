import pandas as pd
import re
from datetime import date

from base_worker import BaseWorker


class ReadCSVComments(BaseWorker):
    '''
    Class to specifically read in the first four reputation sources as these all had comments in the headers.
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
        self.column_matcher = re.compile("# (\w+,)+\w+")
        self.obj = self.s3_resource.Object(bucket_name=self.bucket,
                                           key=self.key)
        self.today = date.today().strftime('%Y-%m-%d')
        self.df = pd.DataFrame()

    def get_rep_file_from_s3(self):
        column_list = []
        value_list = []
        columns = ''

        for raw_line in self.obj.get()['Body'].iter_lines():
            line = raw_line.decode('utf-8')
            if line.startswith('#'):
                if self.column_matcher.match(line):
                    line = line[1:].strip()
                    columns = line.split(",")
                    for i in columns:
                        column_list.append(i)
                continue
            if columns == '':
                print("FAILURE")
            values = re.findall("\"(.*?)\"", line)
            if len(values) != len(columns):
                values = line.split(",")
            value_list.append(values)

        self.df = pd.DataFrame(value_list, columns=column_list)

    def run_all(self):
        self.get_rep_file_from_s3()
        return self.df
