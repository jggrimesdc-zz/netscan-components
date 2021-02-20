CREATE TABLE meta.request_count
(
    scan_id   text,
    timestamp timestamp,
    count     int,
    PRIMARY KEY (scan_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
