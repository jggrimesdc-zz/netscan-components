import io
import requests
from datetime import date
from zipfile import ZipFile

from base_worker import BaseWorker


class IngestFiles(BaseWorker):

    def __init__(self, source, label, file, config, df=None):
        self.source = source
        self.label = label
        self.file = file
        self.config = config
        self.bucket = self.config.bucket
        self.s3_client = self.config.s3_client
        self.prefix = 'raw'

    def save_files(self):
        if not self.file['is_zip']:
            body = requests.get(self.file['url']).content
            self.s3_client.put_object(
                Body=body,
                Bucket=self.bucket,
                Key=f"{self.prefix}/{self.source}/{self.label}/{self.label}-{date.today()}{self.file['file_type']}"
            )
        else:
            zipped_body = ZipFile(io.BytesIO(requests.get(self.file['url']).content))
            for name in zipped_body.namelist():
                self.s3_client.put_object(
                    Body=zipped_body.read(name),
                    Bucket=self.bucket,
                    Key=f"{self.prefix}/{self.source}/{self.label}/{self.label}-{date.today()}{self.file['file_type']}"
                )

    def run_all(self):
        self.save_files()
