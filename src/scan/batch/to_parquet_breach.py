import fastparquet as fp
import s3fs

from base_worker import BaseWorker


class DataframeToParquetBreach(BaseWorker):

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.s3_resource = config.s3_resource
        self.config = config
        self.bucket = self.config.bucket
        self.target_path = f"conformed/{self.source}/{self.label}{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
        self.partitions = self.file['partition_cols']
        self.s3 = s3fs.S3FileSystem()
        self.myopen = self.s3.open

        # added for success file
        self.success_file_key = 'config/_SUCCESS'
        self.success_file_path = f"conformed/{self.source}/{self.label}{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}/_SUCCESS"
        self.success_file = {
            'Bucket': self.bucket,
            'Key': self.success_file_key
        }

    def df_to_parquet(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket)
        bucket.objects.filter(Prefix=self.target_path).delete()

        fp.write(f"s3://{self.bucket}/{self.target_path}/",
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
