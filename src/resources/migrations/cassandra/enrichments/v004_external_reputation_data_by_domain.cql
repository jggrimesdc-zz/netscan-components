CREATE TABLE enrichments.external_reputation_data_by_domain
(
    domain         text,
    timestamp      timestamp,
    effective_from text,
    id             text,
    ip             text,
    last_seen      text,
    port           text,
    reported_by    text,
    source         text,
    ssl_sha        text,
    status         text,
    tags           text,
    threat         text,
    url            text,
    PRIMARY KEY (domain, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
