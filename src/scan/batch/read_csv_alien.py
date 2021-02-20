import pandas as pd
import re
from datetime import date

from base_worker import BaseWorker


class ReadAlienCSV(BaseWorker):
    '''
    Class to read in the alienvault sourced data. The columns are not defined in the raw data and need to be specified here.
    '''

    def __init__(self, source, label, file, config, df=None):
        self.source = source
        self.label = label
        self.file = file
        self.s3_client = config.s3_client
        self.s3_resource = config.s3_resource
        self.bucket = config.bucket
        self.file_type = self.file['file_type']
        self.columns = self.file['columns']
        self.key = f"raw/{self.source}/{self.label}/{self.label}-{date.today()}{self.file_type}"
        self.obj = self.s3_resource.Object(bucket_name=self.bucket,
                                           key=self.key)
        self.df = pd.DataFrame()

    def get_file_from_s3(self):
        value_list = []

        for raw_line in self.obj.get()['Body'].iter_lines():
            line = raw_line.decode('utf-8').strip()
            if not line:
                continue
            if not line.startswith("#"):
                line = line.replace(" # ", ",")
                # finds the first space before the country (two upper case letters)
                if re.search(r'([A-Z]{2,2},)', line):
                    line = re.sub(r'\s(?=[A-Z]{2,2},)', ',', line)
                # edgecase: finds the first space before uppercase letter and number
                if re.search(r'\s(?=[A-Z][0-9]{1,1},)', line):
                    line = re.sub(r'\s(?=[A-Z][0-9]{1,1},)', ',', line)
                # finds where country and city are both empty
                if re.search(r'\s,,', line):
                    line = re.sub(r'\s,,', ",no_value,no_value,", line)
                # finds where city is empty but country isn't
                if re.search(r'\s,', line):
                    line = re.sub(r'\s,', ",no_value,", line)

                values = line.split(",")
                value_list.append(values)

        self.df = pd.DataFrame(value_list, columns=self.columns)
        self.df = self.df.replace("no_value", "")
        self.df = self.df.replace("", "N/A")

    def run_all(self):
        self.get_file_from_s3()
        return self.df
