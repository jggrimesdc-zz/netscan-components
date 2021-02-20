CREATE TABLE status.by_duns
(
    duns         text,
    timestamp    timestamp,
    scan_user_id text,
    scan_id      text,
    company_name text,
    domain_name  text,
    scan_status  text,
    PRIMARY KEY (duns, timestamp, scan_user_id, scan_id)
) WITH CLUSTERING ORDER BY (timestamp DESC, scan_user_id DESC, scan_id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
