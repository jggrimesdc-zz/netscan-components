import argparse
import json
import logging
import os
import psycopg2
import pyspark.sql.functions as F
import pyspark.sql.types as T
from py4j.protocol import Py4JJavaError
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, split
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, TimestampType

SPARK_CLASSPATH = os.getenv('SPARK_CLASSPATH', '/usr/lib/spark/jars/postgresql-42.2.18.jar')


# logging.basicConfig(format='EMR_THREAT_PROCESSOR-%(levelname)s-%(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucketName', help='bucket name')
    parser.add_argument('--objectKey', help='object key')
    parser.add_argument('--fileSource', help='file source')
    parser.add_argument('--rdsDB', help='rds database')
    parser.add_argument('--rdsHost', help='rds host')
    parser.add_argument('--rdsSchema', help='rds schema')
    parser.add_argument('--rdsUsername', help='rds username')
    parser.add_argument('--rdsPassword', help='rds password')
    return parser.parse_args()


def parse_array_from_string(column):
    try:
        res = json.loads(column)
        return res
    except (TypeError, EOFError):
        pass


def clean_dataframe(raw_df):
    retrieve_array = F.udf(parse_array_from_string, T.ArrayType(T.StringType()))
    retrieve_array_obj = F.udf(parse_array_from_string, ArrayType(StructType([
        StructField("kill_chain_name", StringType(), True),
        StructField("phase_name", StringType(), True)
    ])))

    retrieve_array_refs = F.udf(parse_array_from_string, ArrayType(StructType([
        StructField("description", StringType(), True),
        StructField("external_id", StringType(), True),
        StructField("source_name", StringType(), True),
        StructField("url", StringType(), True)
    ])))

    cleaned_df = raw_df \
        .withColumn("aliases", retrieve_array(F.col("x_mitre_aliases"))) \
        .withColumn("contributors", retrieve_array(F.col("x_mitre_contributors"))) \
        .withColumn("created", col("created").cast(TimestampType())) \
        .withColumn("data_sources", retrieve_array(F.col("x_mitre_data_sources"))) \
        .withColumn("defense_bypassed", retrieve_array(F.col("x_mitre_defense_bypassed"))) \
        .withColumn("effective_permissions", retrieve_array(F.col("x_mitre_effective_permissions"))) \
        .withColumn("ext_references_id", F.lit(-1)) \
        .withColumn("external_refs", retrieve_array_refs(F.col("external_references"))) \
        .withColumn("external_id", col("external_refs").getItem(0).external_id) \
        .withColumn("external_url", col("external_refs").getItem(0).url) \
        .withColumn("impact_type", retrieve_array(F.col("x_mitre_impact_type"))) \
        .withColumn("labels", retrieve_array(F.col("labels"))) \
        .withColumn("kill_chain_phase", retrieve_array_obj(F.col("kill_chain_phases"))) \
        .withColumn("modified", col("modified").cast(TimestampType())) \
        .withColumn("permissions_required", retrieve_array(F.col("x_mitre_permissions_required"))) \
        .withColumn("platforms", retrieve_array(F.col("x_mitre_platforms"))) \
        .withColumn("source_type", split(col("source_ref"), "--").getItem(0)) \
        .withColumn("system_requirements", retrieve_array(F.col("x_mitre_system_requirements"))) \
        .withColumn("target_type", split(col("target_ref"), "--").getItem(0)) \
        .withColumnRenamed("id", "internal_id") \
        .withColumnRenamed("x_mitre_deprecated", "deprecated") \
        .withColumnRenamed("x_mitre_detection", "detection") \
        .withColumnRenamed("x_mitre_is_subtechnique", "is_subtechnique") \
        .withColumnRenamed("x_mitre_network_requirements", "network_requirements") \
        .withColumnRenamed("x_mitre_old_attack_id", "old_attack_id") \
        .withColumnRenamed("x_mitre_remote_support", "remote_support") \
        .withColumnRenamed("x_mitre_shortname", "short_name") \
        .withColumnRenamed("x_mitre_version", "version") \
        .drop(col("x_mitre_aliases")) \
        .drop(col("x_mitre_contributors")) \
        .drop(col("x_mitre_system_requirements")) \
        .drop(col("x_mitre_data_sources")) \
        .drop(col("x_mitre_defense_bypassed")) \
        .drop(col("x_mitre_effective_permissions")) \
        .drop(col("x_mitre_impact_type")) \
        .drop(col("x_mitre_permissions_required")) \
        .drop(col("x_mitre_platforms"))

    return cleaned_df


def process_threat_actor_data():
    conf = SparkConf()
    conf.set('spark.jars', 'file:%s' % SPARK_CLASSPATH)
    conf.set('spark.executor.extraClassPath', SPARK_CLASSPATH)
    conf.set('spark.driver.extraClassPath', SPARK_CLASSPATH)

    context = SparkContext(conf=conf)
    spark = SQLContext(context)
    conn = get_postgres_conn()
    input_path = f's3://{ARGS.bucketName}/{ARGS.objectKey}'

    raw_parquet = spark.read.parquet(input_path)
    cleaned_df = clean_dataframe(raw_parquet)
    id_mappings = fetch_ids_from_rds(spark)

    # merge mapping & cleand df
    merged = cleaned_df.join(id_mappings, cleaned_df.internal_id == id_mappings.internal_source_id, "left")

    raw_df_tech = merged.filter(col("type") == "attack-pattern")
    raw_df_tact = merged.filter(col("type") == "x-mitre-tactic")
    raw_df_group = merged.filter(col("type") == "intrusion-set")
    raw_df_soft = merged.filter((col("type") == "tool") | (col("type") == "malware"))
    raw_df_mitigation = merged.filter(col("type") == "course-of-action")
    raw_df_rel = merged.filter(col("type") == "relationship")

    process_techniques(conn, raw_df_tech)
    process_tactics(conn, raw_df_tact)
    process_groups(conn, raw_df_group)
    process_software(conn, raw_df_soft)
    process_mitigation(conn, raw_df_mitigation)

    rel = process_relationship(raw_df_rel)
    process_relationships(id_mappings, rel)
    # TODO Process external references for each type


def process_relationships(mappings, rel):
    joined_df = rel.join(mappings, rel.source_ref == mappings.internal_source_id, "inner") \
        .withColumnRenamed("id", "source_id") \
        .drop(col("internal_source_id")) \
        .join(mappings, rel.target_ref == mappings.internal_source_id, "inner") \
        .withColumnRenamed("id", "target_id") \
        .drop(col("name")) \
        .drop(col("internal_source_id")) \
        .drop(col("source_ref")) \
        .drop(col("target_ref"))

    write_to_rds(joined_df, "relationship", True)


def fetch_ids_from_rds(spark):
    return read_from_rds(spark, "id_mapping") \
        .withColumnRenamed("internal_id", "internal_source_id")


def process_techniques(conn, tech_df):
    tech_df_s = tech_df.select(
        "id",
        "internal_id",
        "contributors",
        "created",
        "data_sources",
        "defense_bypassed",
        "deprecated",
        "description",
        "detection",
        "ext_references_id",
        "effective_permissions",
        "external_id",
        "external_url",
        "impact_type",
        "is_subtechnique",
        "kill_chain_phase",
        "modified",
        "name",
        "network_requirements",
        "permissions_required",
        "platforms",
        "remote_support",
        "revoked",
        "system_requirements",
        "type",
        "version"
    ) \
        .withColumn("tactics", col("kill_chain_phase.phase_name")) \
        .drop(col("kill_chain_phase"))

    tech_df_new = tech_df_s.filter(col("id").isNull()).drop(col("id"))
    tech_df_modified = tech_df_s.filter(col("id").isNotNull())
    write_to_rds(tech_df_new, "technique")
    upsert_to_rds(conn, tech_df_modified, "technique", "technique_temp")


def process_tactics(conn, tact_df):
    tact_df_x = tact_df.select(
        "id",
        "created",
        "description",
        "external_id",
        "external_url",
        "internal_id",
        "modified",
        "name",
        "short_name",
        "type",
    )
    tech_df_new = tact_df_x.filter(col("id").isNull()).drop(col("id"))
    tech_df_modified = tact_df_x.filter(col("id").isNotNull())
    write_to_rds(tech_df_new, "tactic")
    upsert_to_rds(conn, tech_df_modified, "tactic", "tactic_temp")


def process_groups(conn, group_df):
    group_df_r = group_df.select(
        "aliases",
        "contributors",
        "created",
        "description",
        "external_id",
        "external_url",
        "id",
        "internal_id",
        "modified",
        "name",
        "type",
        "revoked",
        "version"
    )
    tech_df_new = group_df_r.filter(col("id").isNull()).drop(col("id"))
    tech_df_modified = group_df_r.filter(col("id").isNotNull())
    write_to_rds(tech_df_new, "group")
    upsert_to_rds(conn, tech_df_modified, "group", "group_temp")


def process_software(conn, soft_df):
    soft_df_r = soft_df.select(
        "aliases",
        "created",
        "contributors",
        "description",
        "external_id",
        "external_url",
        "id",
        "internal_id",
        "labels",
        "modified",
        "name",
        "platforms",
        "type",
        "revoked",
        "version"
    )
    tech_df_new = soft_df_r.filter(col("id").isNull()).drop(col("id"))
    tech_df_modified = soft_df_r.filter(col("id").isNotNull())
    write_to_rds(tech_df_new, "software")
    upsert_to_rds(conn, tech_df_modified, "software", "software_temp")


def process_mitigation(conn, miti_df):
    miti_df_r = miti_df.select(
        "created",
        "deprecated",
        "description",
        "external_id",
        "external_url",
        "id",
        "internal_id",
        "modified",
        "name",
        "old_attack_id",
        "type",
        "version"
    )
    tech_df_new = miti_df_r.filter(col("id").isNull()).drop(col("id"))
    tech_df_modified = miti_df_r.filter(col("id").isNotNull())
    write_to_rds(tech_df_new, "mitigation")
    upsert_to_rds(conn, tech_df_modified, "mitigation", "mitigation_temp")


def process_relationship(rel_df):
    rel_df_r = rel_df.select(
        "relationship_type",
        "source_ref",
        "source_type",
        "target_ref",
        "target_type",
    )

    return rel_df_r


def write_to_rds(df_write, table, overwrite=False):
    mode = "overwrite" if overwrite else "append"
    logging.info("Attempting to write dataframe to table: %s", table)
    try:
        df_write.write \
            .format("jdbc") \
            .mode(mode) \
            .option("url", f'jdbc:postgresql://{ARGS.rdsHost}/{ARGS.rdsDB}') \
            .option("dbtable", f'{ARGS.rdsSchema}.{table}') \
            .option("user", ARGS.rdsUsername) \
            .option("password", ARGS.rdsPassword) \
            .save()
    except Py4JJavaError as e:
        logging.error("Failed to write dataframe to table: %s, %s", table, e)


def read_from_rds(spark, table):
    logging.info("Attempting to read from table: %s", table)
    try:
        df_read = spark.read \
            .format("jdbc") \
            .option("url", f'jdbc:postgresql://{ARGS.rdsHost}/{ARGS.rdsDB}') \
            .option("dbtable", f'{ARGS.rdsSchema}.{table}') \
            .option("user", ARGS.rdsUsername) \
            .option("password", ARGS.rdsPassword) \
            .load()
        return df_read
    except Py4JJavaError as e:
        logging.error("Failed to read from table: %s, %s", table, e)


def upsert_to_rds(conn, dataframe, table, temp_table):
    write_to_rds(dataframe, temp_table, True)

    table = f"{ARGS.rdsSchema}.{table}"
    temp_table = f"{ARGS.rdsSchema}.{temp_table}"
    columns = dataframe.columns
    temp_columns = ["mod." + col for col in columns]
    columns = ', '.join(columns[1:])
    temp_columns = ', '.join(temp_columns[1:])
    sql = "UPDATE %s AS og SET (%s) = (%s) FROM %s AS mod " \
          "WHERE og.id = mod.id and mod.modified >= og.modified" \
          % (table, columns, temp_columns, temp_table)

    with conn.cursor() as cur:
        cur.execute(sql)


def get_postgres_conn():
    try:
        conn = psycopg2.connect(dbname=ARGS.rdsDB,
                                user=ARGS.rdsUsername,
                                password=ARGS.rdsPassword,
                                host=ARGS.rdsHost)
        return conn
    except psycopg2.OperationalError as e:
        logging.error("ERROR: Unexpected error: Could not connect to PostgreSQL instance. %s", e)
        raise


if __name__ == "__main__":
    ARGS = parse_arguments()
    process_threat_actor_data()
