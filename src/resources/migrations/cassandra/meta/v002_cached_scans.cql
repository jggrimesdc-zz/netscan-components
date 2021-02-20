CREATE TABLE meta.cached_scans
(
    domains   text,
    timestamp timestamp,
    scan_id   text,
    PRIMARY KEY (domains, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'};

