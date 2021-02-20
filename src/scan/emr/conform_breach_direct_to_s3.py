# from pyspark import SparkContext, SparkConf
# from pyspark.sql import SQLContext

# conf = SparkConf()
# sc = SparkContext(conf=conf)
# spark = SQLContext(sc)

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# import packages
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType as T
from pyspark.sql.types import StringType
from pyspark.sql.types import IntegerType
import datetime
import uuid
import json
import sys
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--bucketName', help='bucket name')
parser.add_argument('--objectKey', help='object key')
parser.add_argument('--fileSource', help='file source')
parser.add_argument('--destBucket', help='destination bucket')
parser.add_argument('--destPath', help='destination path')
args = parser.parse_args()


def parse_email(email):
    if '@' in email:
        return (email.split('@')[1])
    return ('unknown-domain')


# get the argument for the S3 filename
obj_key = args.objectKey

if '/' in obj_key:
    filename = obj_key.split('/')[len(obj_key.split('/')) - 1]
else:
    filename = obj_key

# get the args for s3 destination
dest_path = 's3://' + args.destBucket + '/' + args.destPath + filename

# read in data
start = time.time()
input_bucket = 's3://' + args.bucketName
input_path = '/' + obj_key
df = spark.read.json(input_bucket + input_path)
print('TIME TO READ IN FROM S3', str(time.time() - start))

# dedupe the dataframe
df = df.dropDuplicates(df.schema.names)

# create a udf for parsing emails
get_domain_udf = F.udf(parse_email, StringType())

# save column to df_cols
df_cols = df.schema.names

# convert cols to lowercase
for col in df_cols:
    df = df.withColumnRenamed(col, col.lower())

# save column to df_cols
df_cols = df.schema.names

# rename domain if its there or simply add the source_of_breach column
if 'domain' in df_cols:
    df = df.withColumnRenamed('domain', 'source_of_breach')
else:
    df = df.withColumn('source_of_breach', F.lit(filename))

# rename the other columns if any inconsistencies are present
if 'username' in df_cols:
    df = df.withColumnRenamed('username', 'user')
if 'passhash' in df_cols:
    df = df.withColumnRenamed('passhash', 'pass_hash')
if 'passsalt' in df_cols:
    df = df.withColumnRenamed('passsalt', 'pass_salt')
if 'userid' in df_cols:
    df = df.withColumnRenamed('userid', 'user_id')

# replace null or empty domains if they exist
# df = df.fillna('unknown-email',subset=['domain'])
# add a column that is email trimmed
if 'email' in df.schema.names:
    df = df.withColumn("email_trimmed", F.trim(F.col("email")))
    df = df.drop('email')
    df = df.withColumnRenamed('email_trimmed', 'email')
    df = df.fillna('unknown-email', subset=['email'])
    df = df.withColumn("email", F.when(F.col("email") == '', 'unknown-email').otherwise(F.col("email")))
elif 'user' in df.schema.names:
    df = df.withColumn("email_trimmed", F.trim(F.col("user")))
    df = df.drop('user')
    df = df.withColumnRenamed('email_trimmed', 'user')
    df = df.fillna('unknown-email', subset=['user'])
    df = df.withColumn("user", F.when(F.col("user") == '', 'unknown-email').otherwise(F.col("user")))
elif 'name' in df.schema.names:
    df = df.withColumn("email_trimmed", F.trim(F.col("name")))
    df = df.drop('name')
    df = df.withColumnRenamed('email_trimmed', 'name')
    df = df.fillna('unknown-email', subset=['name'])
    df = df.withColumn("name", F.when(F.col("name") == '', 'unknown-email').otherwise(F.col("name")))

# parse out the email before proceeding
if 'email' in df_cols:
    df = df.withColumn("domain", get_domain_udf('email'))
elif 'user' in df_cols:
    df = df.withColumn("domain", get_domain_udf('user'))
    df = df.withColumn("email", df["user"])
elif 'name' in df_cols:
    df = df.withColumn("domain", get_domain_udf('name'))
    df = df.withColumn("name", df["name"])
else:
    df = df.withColumn("domain", F.lit('unknown-domain'))

# save the wcaas native col names
wcaas_col_names = ['domain', 'email', 'user', 'user_id', 'name', 'source', 'ip', 'password', 'pass_hash', 'pass_salt',
                   'source_of_breach']

# save column names to df_cols
df_cols = df.schema.names

cols_to_drop = []
for col in df_cols:
    if col not in wcaas_col_names:
        cols_to_drop.append(col)
df = df.drop(*cols_to_drop)

# save the current time into an object
ts = datetime.datetime.now().isoformat(timespec='seconds')

# create a udf to generate UUIDs
uuidUdf = F.udf(lambda: str(uuid.uuid4()), StringType())

# add any columns that are missing
for col in wcaas_col_names:
    if col not in df_cols:
        df = df.withColumn(col, F.lit(''))

# replace null or empty passwords if they exist
df = df.withColumn("pass_trimmed", F.trim(F.col("password")))
df = df.drop('password')
df = df.withColumnRenamed('pass_trimmed', 'password')
df = df.fillna('unknown-password', subset=['password'])
df = df.withColumn("password", F.when(F.col("password") == '', 'unknown-password').otherwise(F.col("password")))

df = df.withColumn("timestamp", F.lit(ts))
df = df.withColumn("id", uuidUdf())


# trim domains
def trim_string_72_chars(domain):
    if len(domain) > 72:
        return (domain[0:72])
    return (domain)


# create a udf for trimming domains to 72 chars
trim_domain_udf = F.udf(trim_string_72_chars, StringType())

df = df.withColumn('domain', trim_domain_udf('domain'))

# start=time.time()
# #df.write.mode('overwrite').partitionBy('domain').parquet('s3://cyber-reputation-data-dev-qos/processed/' + filename)
# df.write.mode('overwrite').partitionBy('domain').parquet(filename)
# #print('TIME TO WRITE TO S3',str(time.time()-start))
# print('TIME TO WRITE',str(time.time()-start))

num_partitions = 1000
get_hash_udf = F.udf(hash, StringType())
df = df.withColumn("domain_hash", get_hash_udf('domain'))


def create_partition(hash_val):
    return str(hash_val % 1000)


get_part_udf = F.udf(create_partition, StringType())
df = df.withColumn("part", get_part_udf('domain_hash'))

start = time.time()
df.write.mode('overwrite').partitionBy('part').parquet(dest_path)
print('TIME TO WRITE TO S3', str(time.time() - start))
