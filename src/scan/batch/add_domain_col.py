from base_worker import BaseWorker


class AddDomainColumn(BaseWorker):
    '''
    Class to add in a domain column. May be redudnant as the processor code does this for reputation.
    '''

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.config = config
        self.single_col = self.file['single_col'][0]

    def print_df(self):
        print(self.df.head())

    def add_domain_col(self):
        self.df['domain'] = self.df[self.single_col].str.extract(
            r'((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])')

    def run_all(self):
        self.add_domain_col()
        return self.df
