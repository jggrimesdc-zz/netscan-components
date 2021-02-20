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

conf = SparkConf().set("spark.cassandra.connection.host", args.cassandraHost).set("spark.jars",
                                                                                  "spark-cassandra-connector-assembly-2.5.1.jar")
sc = SparkContext(conf=conf)
spark = SQLContext(sc)
# spark.conf.set(s"spark.sql.catalog.mycatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")

# read in data
start_time = time.time()
bucket_name = args.bucketName
object_key = args.objectKey
source_doc = args.fileSource
inputPath = 's3://' + bucket_name + "/" + object_key
print('READING DOCUMENT(S) AT ', inputPath)
df = spark.read.parquet(inputPath)
print('TIME TO READ IN FROM S3: ', str(time.time() - start_time), 's')

# save the current time into an object
ts = datetime.datetime.now().isoformat(timespec='seconds')

# create a udf to generate UUIDs
uuidUdf = F.udf(lambda: str(uuid.uuid4()), StringType())

# standardize columns across all docs
reputation_basis = {
    "id": "",  # {custom}
    "effective_from": "",  # Listingdate, Firstseen, dateadded, submission_time (PhishTank)
    "last_seen": "",  # LastOnline
    "ip": "",  # DstIp, ip
    "port": "",  # DstPort
    "ssl_sha": "",  # SHA1
    "url": "",  # url
    "domain": "",  # {custom}
    "status": "",  # url_status
    "threat": "",  # {custom}, Listingreason, Malware
    "threat_type": "",  # {custom}, threat, type
    "tags": "",  # tags
    "source_of_reputation": "",  # {custom}
    "source_detail_url": "",  # urlhaus_link, phish_detail_url
    "reported_by": "",  # {custom}, reporter
    "timestamp": "",  # {custom}
    "country": "",  # country
    "city": "",  # city
    "lat": "",  # lat
    "long": "",  # long
    "source_system_id": "",  # id, phish_id
    "verified": "",  # verified
    "verification_time": "",  # verification_time
    "online": "",  # online
    "target": ""  # target
}

df_r = df.withColumnRenamed("Listingdate", "effective_from") \
    .withColumnRenamed("Firstseen", "effective_from") \
    .withColumnRenamed("dateadded", "effective_from") \
    .withColumnRenamed("submission_time", "effective_from") \
    .withColumnRenamed("LastOnline", "last_seen") \
    .withColumnRenamed("DstIP", "ip") \
    .withColumnRenamed("DstPort", "port") \
    .withColumnRenamed("SHA1", "ssl_sha") \
    .withColumnRenamed("url_status", "status") \
    .withColumnRenamed("threat", "threat_type") \
    .withColumnRenamed("type", "threat_type") \
    .withColumnRenamed("Listingreason", "threat") \
    .withColumnRenamed("Malware", "threat") \
    .withColumnRenamed("tags", "tags") \
    .withColumnRenamed("urlhaus_link", "source_detail_url") \
    .withColumnRenamed("phish_detail_url", "source_detail_url") \
    .withColumnRenamed("reporter", "reported_by") \
    .withColumnRenamed("id", "source_system_id") \
    .withColumnRenamed("phish_id", "source_system_id")

# add missing columns and remap values as needed
df_r = df_r.withColumn("id", uuidUdf())
df_r = df_r.withColumn("timestamp", F.lit(ts))
if 'url' in df_r.columns:
    df_r = df_r.withColumn('domain', regexp_extract(col('url'),
                                                    '(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]',
                                                    0))
if 'threat' not in df_r.columns:
    df_r = df_r.withColumn('threat', F.lit(source_doc))
else:
    df_r = df_r.withColumn('threat', F.lit(source_doc + " - ") + col('threat'))
if 'source_of_reputation' not in df_r.columns:
    df_r = df_r.withColumn('source_of_reputation', F.lit(source_doc))
else:
    df_r = df_r.withColumn('source_of_reputation', F.lit(source_doc + " - ") + col('source_of_reputation'))
if 'reported_by' not in df_r.columns:
    df_r = df_r.withColumn('reported_by', col('source_of_reputation'))

for col in df_r.schema.names:
    if col not in reputation_basis:
        print("DROPPING COLUMN ", col)
        df_r = df_r.drop(col)

for key in list(reputation_basis.keys()):
    if key not in df_r.schema.names:
        print("ADDING EMPTY COLUMN ", key)
        df_r = df_r.withColumn(key, F.lit(''))

df_r.show()
# insert data into wcaas
df_domain = df_r.filter(df_r.domain.isNotNull())
df_domain = df_domain.filter("domain != ''")
if df_domain.count() > 0:
    start_time = time.time()
    df_domain.write.format("org.apache.spark.sql.cassandra").mode('append').options(
        table="external_reputation_by_domain", keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_reputation_by_domain: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_reputation_by_domain')

df_ip = df_r.filter(df_r.ip.isNotNull())
df_ip = df_ip.filter("ip != ''")
if df_ip.count() > 0:
    start_time = time.time()
    df_ip.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="external_reputation_by_ip",
                                                                                keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_reputation_by_ip: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_reputation_by_ip')

df_ssl = df_r.filter(df_r.ssl_sha.isNotNull())
df_ssl = df_ssl.filter("ssl_sha != ''")
if df_ssl.count() > 0:
    start_time = time.time()
    df_ssl.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="external_reputation_by_ssl_sha",
                                                                                 keyspace="enrichments").save()
    print('TIME TO WRITE TO enrichments.external_reputation_by_ssl_sha: ', str(time.time() - start_time), 's')
else:
    print('NO DATA TO WRITE FOR enrichments.external_reputation_by_ssl_sha')
