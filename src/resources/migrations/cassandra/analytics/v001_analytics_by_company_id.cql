CREATE TABLE analytics.by_company_id
(
    company_id   text,
    timestamp    timestamp,
    company_info text,
    domains      text,
    duns         int,
    ip_address   text,
    scan_user_id text,
    PRIMARY KEY (company_id, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
