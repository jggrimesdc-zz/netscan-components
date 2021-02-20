CREATE TABLE meta.meta_data
(
    scan_id         text,
    scan_user_id    text,
    start_time      timestamp,
    end_time        timestamp,
    company_name    text,
    domain          text,
    duns            text,
    s3_raw_dump_url text,
    PRIMARY KEY ((scan_id, scan_user_id),
    start_time,
    end_time
) ) WITH CLUSTERING ORDER BY (start_time DESC, end_time DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
