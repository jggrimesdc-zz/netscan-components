import argparse
import json
import psycopg2
import pyspark.sql.functions as f
import pyspark.sql.types as t
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType

spark = SparkSession.builder.getOrCreate()


def parse_array_from_string(x):
    res = json.loads(x)
    return res


def clean_string(value):
    value = value.strip().lower()
    return value


# get python arguments
parser = argparse.ArgumentParser()
parser.add_argument('--bucketName', help='bucket name')
parser.add_argument('--objectKey', help='object key')
parser.add_argument('--fileSource', help='file source')
parser.add_argument('--rdsHost', help='rds host')
parser.add_argument('--rdsDB', help='rds default database')
parser.add_argument('--rdsSchema', help='rds target schema')
parser.add_argument('--rdsTable', help='rds target table')
parser.add_argument('--rdsUsername', help='rds username')
parser.add_argument('--rdsPassword', help='rds password')
args = parser.parse_args()

# initialize env variables as objects
source = args.fileSource
bucket = args.bucketName
obj_key = args.objectKey
rds_host = args.rdsHost
rds_db = args.rdsDB
rds_schema = args.rdsSchema
rds_table = args.rdsTable
rds_user = args.rdsUsername
rds_pass = args.rdsPassword

# create UDFs
retrieve_array = f.udf(parse_array_from_string, t.ArrayType(t.StringType()))

# ingest conformed data from s3
source_path = f"s3://{bucket}/{obj_key}"
df = spark.read.parquet(source_path)

# cast last_updated to datetime
df = df.withColumn('last_updated',
                   f.to_date(f.unix_timestamp(f.col('last_updated'), 'yyyy-MM-dd').cast("timestamp")))

# create a view to query the data
df.createOrReplaceTempView("tools")

# get the most recent occurance of each record
df = spark.sql('''
    SELECT 
        *
    FROM (
        SELECT 
            *,
            dense_rank() OVER (PARTITION BY name ORDER BY last_updated DESC) AS rank
        FROM tools
    ) vo WHERE rank = 1
''')

# drop the index column
columns_to_drop = ['index', 'last_updated', 'rank']
df = df.drop(*columns_to_drop)

# cast list columns to arrays
df = df.withColumn("category", retrieve_array(f.col("category")))
df = df.withColumn("arch", retrieve_array(f.col("arch")))
df = df.withColumn("depends", retrieve_array(f.col("depends")))
df = df.withColumn("dlagents", retrieve_array(f.col("dlagents")))
df = df.withColumn("sha512sums", retrieve_array(f.col("sha512sums")))

# read in the current tools table from pg
current_tools_table = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{rds_host}/{rds_db}") \
    .option("dbtable", f"{rds_schema}.{rds_table}") \
    .option("user", rds_user) \
    .option("password", rds_pass) \
    .load()

# convert the column names of the incoming table to uppercase
for col in df.schema.names:
    df = df.withColumnRenamed(col, col.upper())

# keep only the column from current tools that I need
current_tools_table = current_tools_table.select(['ID', 'NAME', 'SOURCE_OF_TOOL'])

# create aliases of the dataframes
df_a = df.alias('df_a')
ct_a = current_tools_table.alias('ct_a')

# rename the columns of one of the dataframes to avoid duplicate columns in the other dataframes
ct_a = ct_a.withColumnRenamed('NAME', 'ct_NAME')
ct_a = ct_a.withColumnRenamed('SOURCE_OF_TOOL', 'ct_SOURCE_OF_TOOL')

# inner join the existing and incoming data on the name and source of tool column
temp_df = ct_a.join(df_a, (ct_a.ct_NAME == df_a.NAME) & (ct_a.ct_SOURCE_OF_TOOL == df_a.SOURCE_OF_TOOL), how='inner')

# get the existing names as a list
existing_names = [r[0] for r in temp_df.select('ct_NAME').toLocalIterator()]

# identify new tools by comparing incoming data with existing names
new_tools_df = df_a.filter(~df_a.NAME.isin(existing_names))
new_tools_df = new_tools_df.withColumn('ID', f.lit(-1))

# drop unneeded columns
columns_to_drop = ['NAME', 'SOURCE_OF_TOOL']
temp_df = temp_df.drop(*columns_to_drop)

# rename some columns
temp_df = temp_df.withColumnRenamed('ct_NAME', 'NAME')
temp_df = temp_df.withColumnRenamed('ct_SOURCE_OF_TOOL', 'SOURCE_OF_TOOL')

# rearrange the columns in this dataframe
temp_df = temp_df.select(
    "CATEGORY",
    "DESCRIPTION",
    "PACKAGE_URL",
    "AUTHOR",
    "LICENSE",
    "PACKAGE_VERSION",
    "PACKAGE_RELEASE",
    "ARCH",
    "DEPENDS",
    "DLAGENTS",
    "SHA512SUMS",
    "SOURCE_OF_TOOL",
    "NAME",
    "ID"
)

ready_for_db = temp_df.union(new_tools_df)

temp_table_name = 'tools_temp'

# write ready_for_db to a temp table in pg
ready_for_db.write \
    .mode('overwrite') \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{rds_host}/{rds_db}") \
    .option("dbtable", f"{rds_schema}.{temp_table_name}") \
    .option("user", rds_user) \
    .option("password", rds_pass) \
    .save()

# Attempt to connect to RDS instance
try:
    conn = psycopg2.connect(dbname=rds_db,
                            user=rds_user,
                            password=rds_pass,
                            host=rds_host)
except psycopg2.OperationalError as e:
    print("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
    raise

cur = conn.cursor()

cur.execute('''
    UPDATE tool.tool AS tm
    SET
        "CATEGORY" = tt."CATEGORY",
        "DESCRIPTION" = tt."DESCRIPTION",
        "PACKAGE_URL" = tt."PACKAGE_URL",
        "AUTHOR" = tt."AUTHOR", 
        "LICENSE" = tt."LICENSE",
        "PACKAGE_VERSION" = tt."PACKAGE_VERSION",
        "PACKAGE_RELEASE" = tt."PACKAGE_RELEASE",
        "ARCH" = tt."ARCH",
        "DEPENDS" = tt."DEPENDS",
        "DLAGENTS" = tt."DLAGENTS",
        "SHA512SUMS" = tt."SHA512SUMS"
    FROM tool.tools_temp AS tt
    WHERE tm."ID" = tt."ID";
'''
            )

cur.execute('''
    INSERT INTO tool.tool AS tm
        (
            "NAME",
            "CATEGORY",
            "DESCRIPTION",
            "PACKAGE_URL",
            "AUTHOR",
            "LICENSE",
            "PACKAGE_VERSION",
            "PACKAGE_RELEASE",
            "ARCH",
            "DEPENDS",
            "DLAGENTS",
            "SHA512SUMS",
            "SOURCE_OF_TOOL"
        )
    SELECT 
    "NAME",
    "CATEGORY",
    "DESCRIPTION",
    "PACKAGE_URL",
    "AUTHOR",
    "LICENSE",
    "PACKAGE_VERSION",
    "PACKAGE_RELEASE",
    "ARCH",
    "DEPENDS",
    "DLAGENTS",
    "SHA512SUMS",
    "SOURCE_OF_TOOL"
    FROM tool.tools_temp AS tt
    WHERE tt."ID" = -1;
'''
            )

conn.commit()
cur.close()
conn.close()

# read in tools table and mitre software to update the crosswalk
tools_table = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{rds_host}/{rds_db}") \
    .option("dbtable", f"{rds_schema}.{rds_table}") \
    .option("user", rds_user) \
    .option("password", rds_pass) \
    .load()

mitre_software = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{rds_host}/{rds_db}") \
    .option("dbtable", f"threat_actor.software") \
    .option("user", rds_user) \
    .option("password", rds_pass) \
    .load()

# normalize all column names (uppercase for everything)
for col in mitre_software.schema.names:
    mitre_software = mitre_software.withColumnRenamed(col, col.upper())

# select only the columns I need
mitre_software = mitre_software.select('ID', 'NAME')
tools_table = tools_table.select('ID', 'NAME')

# normalize all the name columns; cast everything to lowercase, trim whitespace off the ends
clean_string_udf = f.udf(clean_string, StringType())

# apply the normalization to the string names
mitre_software = mitre_software.withColumn("NAME", clean_string_udf('NAME'))
tools_table = tools_table.withColumn("NAME", clean_string_udf('NAME'))

# create aliases for both tables
mt_a = mitre_software.alias('mt_a')
tt_a = tools_table.alias('tt_a')

# alter the names of columns in one table to avoid duplicates on the merged product
tt_a = tt_a.withColumnRenamed('ID', 'tt_ID')
tt_a = tt_a.withColumnRenamed('NAME', 'tt_NAME')

temp_xref_df = tt_a.join(mt_a, mt_a.NAME == tt_a.tt_NAME, how='inner')

# drop unneeded columns
columns_to_drop = ['tt_NAME', 'NAME']
temp_xref_df = temp_xref_df.drop(*columns_to_drop)

# alter the names of columns in one table to avoid duplicates on the merged product
temp_xref_df = temp_xref_df.withColumnRenamed('tt_ID', 'TOOL_ID')
temp_xref_df = temp_xref_df.withColumnRenamed('ID', 'MITRE_SOFTWARE_ID')

# current xref table 
current_xref_table = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{rds_host}/{rds_db}") \
    .option("dbtable", f"{rds_schema}.mitre_crosswalk") \
    .option("user", rds_user) \
    .option("password", rds_pass) \
    .load()

current_xref_table = current_xref_table.withColumnRenamed('MITRE_SOFTWARE_ID', 'ct_MITRE_SOFTWARE_ID')
current_xref_table = current_xref_table.withColumnRenamed('TOOL_ID', 'ct_TOOL_ID')

tm_x = temp_xref_df.alias('tm_x')
ct_x = current_xref_table.alias('ct_x')

temp_df = ct_x.join(tm_x, (ct_x.ct_TOOL_ID == tm_x.TOOL_ID) & (ct_x.ct_MITRE_SOFTWARE_ID == tm_x.MITRE_SOFTWARE_ID),
                    how='inner')

columns_to_drop = ['ct_TOOL_ID', 'ct_MITRE_SOFTWARE_ID']
temp_df = temp_df.drop(*columns_to_drop)

existing_tool_ids = [r[0] for r in temp_df.select('TOOL_ID').toLocalIterator()]
existing_mitre_ids = [r[0] for r in temp_df.select('MITRE_SOFTWARE_ID').toLocalIterator()]

new_xref_df = tm_x.filter((~tm_x.TOOL_ID.isin(existing_tool_ids)) & (~tm_x.MITRE_SOFTWARE_ID.isin(existing_mitre_ids)))
new_xref_df = new_xref_df.withColumn('ID', f.lit(-1))

temp_df = temp_df.select(
    "ID",
    "TOOL_ID",
    "MITRE_SOFTWARE_ID"
)

new_xref_df = new_xref_df.select(
    "ID",
    "TOOL_ID",
    "MITRE_SOFTWARE_ID"
)

ready_for_db = temp_df.union(new_xref_df)

temp_table_name = 'tools_xref_temp'

# write ready_for_db to a temp table in pg
ready_for_db.write \
    .mode('overwrite') \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{rds_host}/{rds_db}") \
    .option("dbtable", f"{rds_schema}.{temp_table_name}") \
    .option("user", rds_user) \
    .option("password", rds_pass) \
    .save()

# Attempt to connect to RDS instance
try:
    conn = psycopg2.connect(dbname=rds_db,
                            user=rds_user,
                            password=rds_pass,
                            host=rds_host)
except psycopg2.OperationalError as e:
    print("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
    raise

cur = conn.cursor()

cur.execute('''
    UPDATE tool.mitre_crosswalk AS tm
    SET
        "TOOL_ID" = tt."TOOL_ID",
        "MITRE_SOFTWARE_ID" = tt."MITRE_SOFTWARE_ID"
    FROM tool.tools_xref_temp AS tt
    WHERE tm."ID" = tt."ID";
'''
            )

cur.execute('''
    INSERT INTO tool.mitre_crosswalk AS tm
        (
            "TOOL_ID",
            "MITRE_SOFTWARE_ID"
        )
    SELECT 
        "TOOL_ID",
        "MITRE_SOFTWARE_ID"
    FROM tool.tools_xref_temp AS tt
    WHERE tt."ID" = -1;
'''
            )

conn.commit()
cur.close()
conn.close()
