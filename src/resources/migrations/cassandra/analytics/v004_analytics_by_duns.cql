CREATE TABLE analytics.by_duns
(
    duns         int,
    timestamp    timestamp,
    company_id   text,
    company_info text,
    domains      text,
    scan_user_id text,
    PRIMARY KEY (duns, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
