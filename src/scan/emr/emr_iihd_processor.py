# import packages
import argparse
import datetime
import time
import uuid
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_extract, col
from pyspark.sql.types import StringType

parser = argparse.ArgumentParser()
parser.add_argument('--bucketName', help='bucket name')
parser.add_argument('--objectKey', help='object key')
parser.add_argument('--fileSource', help='file source')
parser.add_argument('--cassandraHost', help='cassandra ip')
parser.add_argument('--jar', help='jar')
args = parser.parse_args()

conf = SparkConf().set("spark.cassandra.connection.host", args.cassandraHost).set("spark.jars", args.jar)
sc = SparkContext(conf=conf)
spark = SQLContext(sc)

# read in daily data
start_time = time.time()
bucket_name = args.bucketName
object_key = args.objectKey
# source_doc = args.fileSource
inputPath = 's3://' + bucket_name + "/" + object_key
print('READING DOCUMENT(S) AT ', inputPath)
df = spark.read.parquet(inputPath)
print('TIME TO READ IN FROM S3: ', str(time.time() - start_time), 's')

# normalize daily column names
df = df.withColumnRenamed("risk", "risk_id") \
    .withColumnRenamed("asn", "asn_id") \
    .withColumnRenamed("country", "country_code")

# read in risk data
start_time = time.time()
risk_input_path = 's3://' + bucket_name + "/conformed/iihd/cybergreen_risk/cybergreen_risk.json/"
print('READING DOCUMENT(S) AT ', risk_input_path)
df_risk = spark.read.parquet(risk_input_path)
print('TIME TO READ IN FROM S3: ', str(time.time() - start_time), 's')

# normalize risk column names
df_risk = df_risk.withColumnRenamed("title", "risk_title") \
    .withColumnRenamed("id", "risk_id") \
    .withColumnRenamed("slug", "risk_slug") \
    .withColumnRenamed("is_archived", "risk_is_archived") \
    .withColumnRenamed("measurement_units", "risk_measurement_units") \
    .withColumnRenamed("amplification_factor", "risk_amplification_factor") \
    .withColumnRenamed("description", "risk_description") \
    .withColumnRenamed("taxonomy", "risk_taxonomy")

# read in asn data
start_time = time.time()
asn_input_path = 's3://' + bucket_name + "/conformed/iihd/cybergreen_asn/cybergreen_asn.json/"
print('READING DOCUMENT(S) AT ', asn_input_path)
df_asn = spark.read.parquet(asn_input_path)
print('TIME TO READ IN FROM S3: ', str(time.time() - start_time), 's')

# normalize asn column names
df_asn = df_asn.withColumnRenamed("title", "asn") \
    .withColumnRenamed("number", "asn_id")

# drop country column so there is no redundancy
df_asn = df_asn.drop(col("country"))

# join the daily and risk dataframes
df_iihd = df.join(df_risk, ["risk_id"])

# join the daily and asn dataframes
df_iihd = df_iihd.join(df_asn, ["asn_id"])

# save the current time into an object
ts = datetime.datetime.now().isoformat(timespec='seconds')

# create a udf to generate UUids
uuidUdf = F.udf(lambda: str(uuid.uuid4()), StringType())

# standardize columns across all docs
iihd_basis = {
    "asn": "",  # cybergreen_daily: asn, cybergreen_asn: title
    "asn_id": "",  # cybergreen_daily: asn, cybergreen_asn: number
    "id": "",  # {custom}
    "timestamp": "",  # {custom}
    "date": "",  # date
    "country_code": "",  # country
    "count": "",  # count
    "count_amplified": "",  # count_amplified
    "risk_title": "",  # cybergreen_risk: title
    "risk_id": "",  # cybergreen_risk: id, cybergreen_daily: risk
    "risk_slug": "",  # cybergreen_risk: slug
    "risk_is_archived": "",  # cybergreen_risk: is_archived
    "risk_taxonomy": "",  # cybergreen_risk: taxonomy
    "risk_measurement_units": "",  # cybergreen_risk: measurement_units
    "risk_amplification_factor": "",  # cybergreen_risk: amplification_factor
    "risk_description": ""  # cybergreen_risk: description
}

# add missing columns and remap values as needed
df_iihd = df_iihd.withColumn("id", uuidUdf())
df_iihd = df_iihd.withColumn("timestamp", F.lit(ts))

for col in df_iihd.schema.names:
    if col not in iihd_basis:
        print("DROPPING COLUMN ", col)
        df_iihd = df_iihd.drop(col)

for key in list(iihd_basis.keys()):
    if key not in df_iihd.schema.names:
        print("ADDING EMPTY COLUMN ", key)
        df_iihd = df_iihd.withColumn(key, F.lit(''))

# df_iihd.show()

# insert country data into wcaas
df_country_code = df_iihd.filter(df_iihd.country_code.isNotNull())
df_country_code = df_country_code.filter("country_code != ''")
if df_country_code.count() > 0:
    start_time = time.time()
    df_country_code.write.format("org.apache.spark.sql.cassandra").mode('append').options(
        table="external_iihd_by_country", keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_iihd_by_country: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_iihd_by_country')
    # comment per Rigo - Might be a good candidate to functionalize for ease of testing.

# insert risk data into wcaas
df_risk = df_iihd.filter(df_iihd.risk_title.isNotNull())
df_risk = df_risk.filter("risk_title != ''")
if df_risk.count() > 0:
    start_time = time.time()
    df_risk.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="external_iihd_by_risk",
                                                                                  keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_iihd_by_risk: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_iihd_by_risk')

# insert asn data into wcaas
df_asn = df_iihd.filter(df_iihd.asn.isNotNull())
df_asn = df_asn.filter("asn != ''")
if df_asn.count() > 0:
    start_time = time.time()
    df_asn.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="external_iihd_by_asn",
                                                                                 keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_iihd_by_asn: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_iihd_by_asn')

# insert date data into wcaas
df_date = df_iihd.filter(df_iihd.date.isNotNull())
df_date = df_date.filter("date != ''")
if df_date.count() > 0:
    start_time = time.time()
    df_date.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="external_iihd_by_date",
                                                                                  keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_iihd_by_date: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_iihd_by_date')

# insert count data into wcaas
df_count = df_iihd.filter(df_iihd["count"].isNotNull())
# df_count.show()
# df_count = df_count.filter("count != ''")
if df_count.count() > 0:
    start_time = time.time()
    df_count.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="external_iihd_by_count",
                                                                                   keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_iihd_by_count: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_iihd_by_count')

# insert count_amplified data into wcaas
df_count_amplified = df_iihd.filter(df_iihd.count_amplified.isNotNull())
df_count_amplified.show()
# df_count_amplified = df_count_amplified.filter("count_amplified != ''")
if df_count_amplified.count() > 0:
    start_time = time.time()
    df_count_amplified.write.format("org.apache.spark.sql.cassandra").mode('append').options(
        table="external_iihd_by_count_amplified", keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_iihd_by_count_amplified: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_iihd_by_count_amplified')
