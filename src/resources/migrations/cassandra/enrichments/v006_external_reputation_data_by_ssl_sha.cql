CREATE TABLE enrichments.external_reputation_data_by_ssl_sha
(
    ssl_sha        text,
    timestamp      timestamp,
    domain         text,
    effective_from text,
    id             text,
    ip             text,
    last_seen      text,
    port           text,
    reported_by    text,
    source         text,
    status         text,
    tags           text,
    threat         text,
    url            text,
    PRIMARY KEY (ssl_sha, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
