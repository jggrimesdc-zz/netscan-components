import datetime
import pandas as pd
import re
import string
import time
import uuid

from base_worker import BaseWorker

pd.set_option("display.max_columns", 101)


def parse_email(email):
    if '@' in email:
        return (email.split('@')[1])
    return ('unknown-domain')


def trim_string_72_chars(domain):
    if len(domain) > 72:
        return (domain[0:72])
    return (domain)


def create_partition(hash_val):
    return str(hash_val % 1000)


def make_uuid(val):
    return str(uuid.uuid4())


def remove_bad_encodings(value):
    return (value.encode('utf-8', 'replace').decode('utf-8'))


# functions for password traits
def pass_length(pass_value):
    if pass_value == 'unknown-password':
        return -1
    else:
        return len(pass_value)


def pass_character_set(pass_value):
    if pass_value == 'unknown-password':
        return 'unknown-password'
    else:
        digit = 0
        lower = 0
        upper = 0
        special = 0

        for letter in pass_value:
            if letter in string.digits:
                digit += 1
            elif letter in string.ascii_lowercase:
                lower += 1
            elif letter in string.ascii_uppercase:
                upper += 1
            else:
                special += 1
        # Determine character-set
        if digit and not lower and not upper and not special:
            charset = 'numeric'
        elif not digit and lower and not upper and not special:
            charset = 'loweralpha'
        elif not digit and not lower and upper and not special:
            charset = 'upperalpha'
        elif not digit and not lower and not upper and special:
            charset = 'special'

        elif not digit and lower and upper and not special:
            charset = 'mixedalpha'
        elif digit and lower and not upper and not special:
            charset = 'loweralphanum'
        elif digit and not lower and upper and not special:
            charset = 'upperalphanum'
        elif not digit and lower and not upper and special:
            charset = 'loweralphaspecial'
        elif not digit and not lower and upper and special:
            charset = 'upperalphaspecial'
        elif digit and not lower and not upper and special:
            charset = 'specialnum'

        elif not digit and lower and upper and special:
            charset = 'mixedalphaspecial'
        elif digit and not lower and upper and special:
            charset = 'upperalphaspecialnum'
        elif digit and lower and not upper and special:
            charset = 'loweralphaspecialnum'
        elif digit and lower and upper and not special:
            charset = 'mixedalphanum'
        else:
            charset = 'all'
        return (charset)


def pass_complexity_digit(pass_value):
    if pass_value == 'unknown-password':
        return -1
    else:
        return len(re.sub("[^0-9]", "", pass_value))


def pass_complexity_lower(pass_value):
    if pass_value == 'unknown-password':
        return -1
    else:
        return len(re.sub("[^a-z]", "", pass_value))


def pass_complexity_upper(pass_value):
    if pass_value == 'unknown-password':
        return -1
    else:
        return len(re.sub("[^A-Z]", "", pass_value))


def pass_complexity_special(pass_value):
    if pass_value == 'unknown-password':
        return -1
    else:
        return len(re.sub("[0-9A-Za-z]", "", pass_value))


def pass_simple_mask(pass_value):
    if pass_value == 'unknown-password':
        return 'unknown-password'
    else:
        simple_mask = []

        for letter in pass_value:
            if letter in string.digits:
                if not simple_mask or not simple_mask[-1] == 'digit':
                    simple_mask.append('digit')
            elif letter in string.ascii_lowercase:
                if not simple_mask or not simple_mask[-1] == 'string':
                    simple_mask.append('string')
            elif letter in string.ascii_uppercase:
                if not simple_mask or not simple_mask[-1] == 'string':
                    simple_mask.append('string')
            else:
                if not simple_mask or not simple_mask[-1] == 'special':
                    simple_mask.append('special')

        simplemask_string = ''.join(simple_mask) if len(simple_mask) <= 3 else 'othermask'
        return simplemask_string


def pass_advanced_mask(pass_value):
    if pass_value == 'unknown-password':
        return 'unknown-password'
    else:
        advancedmask_string = ""

        for letter in pass_value:
            if letter in string.digits:
                advancedmask_string += "?d"
            elif letter in string.ascii_lowercase:
                advancedmask_string += "?l"
            elif letter in string.ascii_uppercase:
                advancedmask_string += "?u"
            else:
                advancedmask_string += "?s"

        return advancedmask_string


class EmailUpdate(BaseWorker):
    '''
    Class for prepping breach dataframes for extra transformations and parquet write 
    '''

    def __init__(self, source, label, file, config, df):
        self.df = df
        self.source = source
        self.label = label
        self.file = file
        self.config = config
        self.email_col = self.file['email_col']

    def update_email(self):
        # replace null or empty domains if they exist

        df = self.df.copy()

        df[self.email_col] = df[self.email_col].str.strip()
        df[self.email_col] = df[self.email_col].fillna('unknown-email')
        df[self.email_col] = df[self.email_col].replace(r'^\s*$', 'unknown-email', regex=True)
        df['email'] = df[self.email_col]

        df['domain'] = df['email'].apply(parse_email)

        # save the wcaas native col names
        wcaas_col_names = ['domain', 'email', 'user', 'user_id', 'name', 'source', 'ip', 'pass', 'pass_hash',
                           'pass_salt', 'source_of_breach']

        # identify unnecessary columns
        cols_to_drop = []
        for col in df.columns:
            if col not in wcaas_col_names:
                cols_to_drop.append(col)

        # drop any extra columns
        df = df.drop(columns=cols_to_drop)

        # add any columns that are missing
        for col in wcaas_col_names:
            if col not in df.columns:
                df[col] = ''

        # replace null or empty passwords if they exist
        df['pass'] = df['pass'].str.strip()
        df['pass'] = df['pass'].fillna('unknown-password')
        df['pass'] = df['pass'].replace(r'^\s*$', 'unknown-password', regex=True)

        # trim any domains longer than 72 chars
        df['domain'] = df['domain'].apply(trim_string_72_chars)

        num_partitions = 1000
        df['domain_hash'] = df['domain'].apply(hash)  # df.withColumn("domain_hash",get_hash_udf('domain'))
        df['part'] = df['domain_hash'].apply(create_partition)

        # save the current time into an object
        ts = datetime.datetime.now().isoformat(timespec='seconds')

        # add the timestamp and id columns
        df['timestamp'] = str(ts)
        # df['id']=df['email'].apply(make_uuid)

        df['id'] = [uuid.uuid4() for _ in range(len(df.index))]
        df['id'] = df['id'].astype(str)

        df['pass_salt'] = df['pass_salt'].apply(remove_bad_encodings)

        # add in the password characteristics
        print("creating pass metadata at " + time.strftime("%H:%M:%S", time.localtime()))
        df['pass_length'] = df['pass'].apply(pass_length)
        df['pass_character_set'] = df['pass'].apply(pass_character_set)
        df['pass_complexity_digit'] = df['pass'].apply(pass_complexity_digit)
        df['pass_complexity_lower'] = df['pass'].apply(pass_complexity_lower)
        df['pass_complexity_upper'] = df['pass'].apply(pass_complexity_upper)
        df['pass_complexity_special'] = df['pass'].apply(pass_complexity_special)
        df['pass_simple_mask'] = df['pass'].apply(pass_simple_mask)
        df['pass_advanced_mask'] = df['pass'].apply(pass_advanced_mask)
        print("finished pass metadata at " + time.strftime("%H:%M:%S", time.localtime()))

        self.df = df.copy()

    def run_all(self):
        self.update_email()
        return self.df
