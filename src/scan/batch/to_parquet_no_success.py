import fastparquet as fp
import s3fs

from base_worker import BaseWorker


class DataframeToParquetNoSuccess(BaseWorker):
    '''
    An alternative to the to_parquet class that triggers the emr processing step. Used primarily for testing purposes.
    '''

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.s3_resource = config.s3_resource
        self.config = config
        self.bucket = self.config.bucket
        self.target_path = f"s3://{self.bucket}/conformed/{self.source}/{self.label}/{self.label}{self.file['file_type']}/"
        self.partitions = self.file['partition_cols']
        self.s3 = s3fs.S3FileSystem()
        self.myopen = self.s3.open

    def df_to_parquet(self):
        fp.write(self.target_path,
                 data=self.df,
                 compression='SNAPPY',
                 open_with=self.myopen,
                 file_scheme='hive',
                 partition_on=self.partitions,
                 mkdirs=lambda x: True)

    def run_all(self):
        self.df_to_parquet()
