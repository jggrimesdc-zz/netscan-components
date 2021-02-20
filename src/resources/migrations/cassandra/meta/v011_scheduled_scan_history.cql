CREATE TABLE meta.scheduled_scan_history
(
    scan_id     text,
    schedule_id text,
    timestamp   timestamp,
    PRIMARY KEY (scan_id)
) WITH compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
