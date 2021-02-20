CREATE TABLE enrichments.external_reputation_data_by_ip
(
    ip             text,
    timestamp      timestamp,
    domain         text,
    effective_from text,
    id             text,
    last_seen      text,
    port           text,
    reported_by    text,
    source         text,
    ssl_sha        text,
    status         text,
    tags           text,
    threat         text,
    url            text,
    PRIMARY KEY (ip, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
