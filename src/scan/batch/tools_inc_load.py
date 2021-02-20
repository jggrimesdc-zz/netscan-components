import fastparquet as fp
import pandas as pd
import s3fs

from base_worker import BaseWorker


class ToolsIncrementalLoad(BaseWorker):

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

    # the method to determine new updates in the dataframe and mark changes from previous ones
    def update_df(self):
        fs = s3fs.core.S3FileSystem()
        s3_path = f"{self.bucket}/conformed/{self.source}/{self.label}/{self.label}{self.file['file_type']}/"
        all_paths_from_s3 = fs.glob(path=s3_path)

        myopen = self.s3.open

        if len(all_paths_from_s3) > 0:
            # use s3fs as the filesystem
            fp_obj = fp.ParquetFile(all_paths_from_s3, open_with=myopen)
            # convert to pandas dataframe
            existing_data = fp_obj.to_pandas()

            existing_data['name'] = existing_data.name.astype(str)

            new_df = self.df

            # create an empty list that will contain partitions to upsert to
            parts_to_upsert = []

            for name in new_df['name'].unique():
                new_data = new_df[new_df['name'] == name].copy()
                print(new_data['last_updated'])
                update_date = new_data['last_updated'][0]

                old_data = existing_data[existing_data['name'] == name].copy()
                old_data['last_updated'] = pd.to_datetime(old_data['last_updated'])
                recent_date = old_data['last_updated'].max()
                old_data = old_data[old_data['last_updated'] == recent_date]

                change_val = ''

                if len(old_data.index) > 0:
                    cols_to_compare = list(old_data.columns)
                    cols_to_compare.remove('last_updated')

                    for col in cols_to_compare:
                        if new_data[col][0] != old_data[col][0]:
                            change_val += f"modified field: {col}; old value: {old_data[col][0]}; new value: {new_data[col][0]}\n"
                    if change_val != '':
                        new_data['last_updated'] = update_date

                        parts_to_upsert.append(old_data)
                        parts_to_upsert.append(new_data)

            new_data = pd.concat(parts_to_upsert)
            new_data['last_updated'] = new_data['last_updated'].astype(str)

            self.df = new_data
            print(existing_data.info())

    def run_all(self):
        self.update_df()
        return self.df
