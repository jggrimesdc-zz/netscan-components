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


def write_to_wc_table(df, table_name, key_space):
    start = time.time()
    df_to_write.write.format("org.apache.spark.sql.cassandra").mode('append').options(table=table_name,
                                                                                      keyspace=key_space).save()
    print(f"TIME TO WRITE TO {table_name} {str(time.time() - start)}s")


parser = argparse.ArgumentParser()
parser.add_argument('--bucketName', help='bucket name')
parser.add_argument('--objectKey', help='object key')
parser.add_argument('--fileSource', help='file source')
parser.add_argument('--destBucket', help='destination bucket name')
parser.add_argument('--destPath', help='destination path')
args = parser.parse_args()

stats_content = ""

# get the filename
# filename = sys.argv[3]
# print(filename)
obj_key = args.objectKey

# filename = obj_key.split('/')[len(obj_key.split('/'))-1]
if '/' in obj_key:
    filename = obj_key.split('/')[len(obj_key.split('/')) - 1]
else:
    filename = obj_key

# get the source destination
source_path = 's3://' + args.destBucket + '/' + args.destPath + filename

start = time.time()
df = spark.read.parquet(source_path)
print('TIME TO READ IN FROM S3', str(time.time() - start), 's')
stats_content = "TIME TO READ IN FROM S3 " + str(time.time() - start) + "\n"

# drop domain_hash and part columns
columns_to_drop = ['domain_hash', 'part', 'index']
df = df.drop(*columns_to_drop)

# count distinct in domain, email, pass
domain_count = df.select('domain').distinct().count()
email_count = df.select('email').distinct().count()
pass_count = df.select('pass').distinct().count()

start_w = time.time()

# write to any table that depends on email
if email_count > 1:
    df_to_write = df.filter(df.email.isNotNull())
    df_to_write = df_to_write.filter("email != ''")

    write_to_wc_table(df_to_write, 'external_breach_by_email', 'enrichments')

# write to any table that depends on password
if pass_count > 1:
    df_to_write = df_to_write.filter("pass != ''")

    # write to pass tables
    write_to_wc_table(df_to_write, 'external_breach_by_pass', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_pass_length', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_pass_complexity', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_pass_character_set', 'enrichments')

# write to any table that depends on domain and password
if domain_count > 1 and pass_count > 1:
    df_to_write = df.filter(df.domain.isNotNull())
    df_to_write = df_to_write.filter("domain != ''")
    df_to_write = df_to_write.filter("pass != ''")

    write_to_wc_table(df_to_write, 'external_breach_by_domain_pass_advanced_mask', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_domain_pass_character_set', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_domain_pass_complexity', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_domain_pass_length', 'enrichments')
    write_to_wc_table(df_to_write, 'external_breach_by_domain_pass_simple_mask', 'enrichments')

print('OVERALL TIME TO WRITE TO WC', str(time.time() - start_w), 's')
