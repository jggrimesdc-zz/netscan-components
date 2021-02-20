CREATE TABLE status.by_scan_status
(
    scan_status  text,
    scan_user_id text,
    timestamp    timestamp,
    scan_id      text,
    company_name text,
    duns         text,
    PRIMARY KEY ((scan_status, scan_user_id),
    timestamp,
    scan_id
) ) WITH CLUSTERING ORDER BY (timestamp DESC, scan_id DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
