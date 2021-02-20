CREATE TABLE status.by_scan_id
(
    scan_id      text,
    timestamp    timestamp,
    company_name text,
    scan_user_id text,
    duns         text,
    scan_status  text,
    PRIMARY KEY (scan_id, timestamp, company_name, scan_user_id)
) WITH CLUSTERING ORDER BY (timestamp DESC, company_name DESC, scan_user_id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
