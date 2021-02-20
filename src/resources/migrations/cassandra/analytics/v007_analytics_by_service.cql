CREATE TABLE analytics.by_service
(
    service      text,
    timestamp    timestamp,
    domains      text,
    duns         text,
    ip_address   text,
    port         text,
    scan_user_id text,
    PRIMARY KEY (service, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
