import boto3
import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from datetime import date

from base_worker import BaseWorker


class IngestKali(BaseWorker):
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
        self.file_type = self.file['file_type']
        self.df = pd.DataFrame()

    def scrape_kali(self):
        # scrape the kali tools homepage
        headers = requests.utils.default_headers()

        # pretend to be google
        headers.update({'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', })
        r = requests.get(self.url, headers=headers)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')

        raw_s3_path = f"{self.prefix}/{self.source}/{self.label}-{date.today()}"

        count = 0
        for tag in soup.find_all("ul", {"class": "lcp_catlist"}):
            for record in tag.find_all('a'):
                package_name = record.get_text().strip()
                path = f"/tmp/{package_name}.{self.file_type}"

                if record.attrs is not None and 'href' in record.attrs:
                    record_url = record.attrs['href']
                    record_r = requests.get(record_url, headers=headers)
                    record_data = record_r.text
                    # record_soup = BeautifulSoup(record_data)

                    s3_object_key = f"{raw_s3_path}/{package_name}.{self.file_type}"

                    with open(path, 'w') as f:
                        f.write(record_data)
                    f.close()
                    response = self.s3_client.upload_file(path, self.bucket, s3_object_key)

                    print(f"wrote {package_name} to s3")

                    count += 1

    def run_all(self):
        self.scrape_kali()
