import json
import requests
from datetime import date
from datetime import timedelta

from base_worker import BaseWorker


class IngestFilesAPIPaginated(BaseWorker):

    def __init__(self, source, label, file, config, df=None):
        self.config = config
        self.source = source
        self.label = label
        self.file = file
        self.bucket = self.config.bucket
        self.s3_client = self.config.s3_client
        self.prefix = "raw"
        self.json_key = self.file['json_key']
        self.page_key = self.file['page_key']
        self.url_addition = self.file['url_addition']

    def save_paginated_files(self):
        limit_number = 10000
        page_number = 1
        end_date = date.today()
        start_date = date.today() - timedelta(days=1)

        url = self.file['url'] + self.url_addition.format(limit_number,
                                                          page_number,
                                                          start_date,
                                                          end_date)
        body = requests.get(url).json()

        if body[self.page_key] > 0:
            result = []
            pages = body[self.page_key]
            print("There are " + str(pages) + " pages of data to ingest")
            for i in range(1, pages + 1):
                print(i)
                new_url = self.file['url'] + self.url_addition.format(limit_number, i, start_date, end_date)
                new_body = requests.get(new_url).json()['results']
                result += new_body
                print(result)

            body_json = bytes(json.dumps(result).encode('UTF-8'))
            self.s3_client.put_object(
                Body=body_json,
                Bucket=self.bucket,
                # TODO: determine the naming nomenclature for this source - should this be cybergreen?
                Key=f"{self.prefix}/{self.source}/{self.label}/{self.label}-{date.today()}{self.file['file_type']}"
            )

        elif body[self.page_key] == 0:
            print("No Cybergreen updates from yesterday")
            exit()

    def run_all(self):
        self.save_paginated_files()
