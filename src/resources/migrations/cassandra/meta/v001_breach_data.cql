CREATE TABLE meta.breach_data
(
    scan_id         text,
    scan_user_id    text,
    timestamp       timestamp,
    email           text,
    breach_list     text,
    s3_raw_dump_url text,
    PRIMARY KEY ((scan_id, scan_user_id),
    timestamp,
    email
) ) WITH CLUSTERING ORDER BY (timestamp DESC, email DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
