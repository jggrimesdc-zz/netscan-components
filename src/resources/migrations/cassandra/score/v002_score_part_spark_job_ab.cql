CREATE TABLE score.score_part_spark_job_ab
(
    scan_id         text,
    scan_user_id    text,
    factor          text,
    timestamp       timestamp,
    cat             text,
    description     text,
    impact          int,
    netscan         int,
    s3_raw_dump_url text,
    score           float,
    PRIMARY KEY ((scan_id, scan_user_id),
    factor,
    timestamp
) ) WITH CLUSTERING ORDER BY (factor DESC, timestamp DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
