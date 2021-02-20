from datetime import date

from base_worker import BaseWorker


class AddDateColumn(BaseWorker):
    '''
    Class that adds in an additional column of just the date. This is helpful for single-column sources that need an additional column
    for partitioning.
    '''

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.config = config

    def add_date(self):
        self.df['date'] = date.today()

    def run_all(self):
        self.add_date()
        return self.df
