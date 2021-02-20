CREATE TABLE status.by_domain
(
    domain_name  text,
    timestamp    timestamp,
    scan_user_id text,
    scan_id      text,
    company_name text,
    duns         text,
    scan_status  text,
    PRIMARY KEY (domain_name, timestamp, scan_user_id, scan_id)
) WITH CLUSTERING ORDER BY (timestamp DESC, scan_user_id DESC, scan_id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
