CREATE TABLE status.by_date_range
(
    scan_start_time timestamp,
    scan_user_id    text,
    scan_id         text,
    company_name    text,
    duns            text,
    duration        text,
    scan_status     text,
    PRIMARY KEY (scan_start_time, scan_user_id, scan_id)
) WITH CLUSTERING ORDER BY (scan_user_id DESC, scan_id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
