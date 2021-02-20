CREATE TABLE analytics.by_port
(
    port         text,
    timestamp    timestamp,
    domains      text,
    duns         text,
    ip_address   text,
    scan_user_id text,
    service      int,
    PRIMARY KEY (port, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
