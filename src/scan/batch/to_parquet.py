import fastparquet as fp
import s3fs

from base_worker import BaseWorker


class DataframeToParquet(BaseWorker):

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.s3_resource = config.s3_resource
        self.bucket = config.bucket
        self.target_path = f"s3://{self.bucket}/conformed/{self.source}/{self.label}/{self.label}{self.file['file_type']}/"
        self.partitions = self.file['partition_cols']
        self.s3 = s3fs.S3FileSystem()
        self.myopen = self.s3.open

        # added for success file
        self.success_file_key = 'config/_SUCCESS'
        self.success_file_path = f"conformed/{self.source}/{self.label}/{self.label}{self.file['file_type']}/_SUCCESS"
        self.success_file = {
            'Bucket': self.bucket,
            'Key': self.success_file_key
        }

    def df_to_parquet(self):
        fp.write(self.target_path,
                 data=self.df,
                 compression='SNAPPY',
                 open_with=self.myopen,
                 file_scheme='hive',
                 partition_on=self.partitions,
                 mkdirs=lambda x: True)

    def success_to_s3(self):
        self.s3_resource.meta.client.copy(self.success_file,
                                          self.bucket,
                                          self.success_file_path)

    def run_all(self):
        self.df_to_parquet()
        self.success_to_s3()
