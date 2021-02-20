CREATE TABLE status.by_company_name
(
    company_name text,
    timestamp    timestamp,
    scan_id      text,
    scan_user_id text,
    duns         text,
    scan_status  text,
    PRIMARY KEY (company_name, timestamp, scan_id, scan_user_id)
) WITH CLUSTERING ORDER BY (timestamp DESC, scan_id DESC, scan_user_id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
