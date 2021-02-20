import pandas as pd

from base_worker import BaseWorker
from base_worker import BaseWorker


class DateColumnUpdates(BaseWorker):

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.config = config
        self.date_col = self.file['date_col']
        # TODO: rename last_seen_date_col
        self.last_seen_date_col = self.file['last_seen_date_col']

    def update_date_col(self):
        self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')
        self.df['date'] = self.df[self.date_col].dt.date
        self.df['date'] = pd.to_datetime(self.df['date'])

        if self.last_seen_date_col in self.df.columns:
            self.df[self.last_seen_date_col] = pd.to_datetime(self.df[self.last_seen_date_col], errors='coerce')

    def run_all(self):
        self.update_date_col()
        return self.df
