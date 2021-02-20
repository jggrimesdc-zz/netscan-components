CREATE TABLE dqm.event_log
(
    event_id       text,
    timestamp      timestamp,
    event_actor    text,
    event_action   text,
    detail         text,
    detail_type    text,
    error_code     text,
    error_message  text,
    event_bus_name text,
    resources      text,
    PRIMARY KEY (event_id, timestamp, event_actor, event_action)
) WITH CLUSTERING ORDER BY (timestamp DESC, event_actor DESC, event_action DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};

