import pandas as pd

from base_worker import BaseWorker


def remove_bad_encodings(value):
    return (value.encode('utf-8', 'replace').decode('utf-8'))


class BreachPrep(BaseWorker):
    '''
    Class for prepping breach dataframes for extra transformations and parquet write 
    '''

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.config = config

    def prep_breach(self):
        # remove bad encodings
        for col in self.df.columns:
            self.df[col] = self.df[col].apply(remove_bad_encodings)

        # deduping logic
        df_length_unduped = len(self.df.index)
        print("The dataframe has " + str(df_length_unduped) + " total rows before deduplicating")

        self.df = self.df.drop_duplicates()

        duplicated_rows = df_length_unduped - len(self.df.index)
        print("There were " + str(len(self.df.index)) + " total rows after deduplicating")
        print("There were " + str(duplicated_rows) + " duplicated rows")

        # convert columns names to lowercase
        self.df.columns = self.df.columns.str.lower()

        if 'domain' in self.df.columns:
            self.df = self.df.rename(columns={'domain': 'source_of_breach'})
        else:
            self.df['source_of_breach'] = self.label

        # rename the other columns if any inconsistencies are present
        if 'username' in self.df.columns:
            self.df = self.df.rename(columns={'username': 'user'})
        if 'passhash' in self.df.columns:
            self.df = self.df.rename(columns={'passhash': 'pass_hash'})
        if 'passsalt' in self.df.columns:
            self.df = self.df.rename(columns={'passsalt': 'pass_salt'})
        if 'userid' in self.df.columns:
            self.df = self.df.rename(columns={'userid': 'user_id'})
        if 'password' in self.df.columns:
            self.df = self.df.rename(columns={'password': 'pass'})

    def run_all(self):
        self.prep_breach()
        return self.df
