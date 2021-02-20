CREATE TABLE score.score_input_spark_job_ab
(
    scan_id         text,
    user_id         text,
    timestamp       timestamp,
    browserv_subset int,
    browserv_total  int,
    dmarc_subset    int,
    dmarc_total     int,
    https_subset    int,
    https_total     int,
    op_subset       int,
    op_total        int,
    s3_raw_dump_url text,
    spf_subset      int,
    spf_total       int,
    wah_subset      int,
    wah_total       int,
    PRIMARY KEY ((scan_id, user_id),
    timestamp
) ) WITH CLUSTERING ORDER BY (timestamp DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
