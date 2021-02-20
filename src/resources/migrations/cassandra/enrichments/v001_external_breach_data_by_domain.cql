CREATE TABLE enrichments.external_breach_data_by_domain
(
    domain           text,
    id               uuid,
    email            text,
    ip               text,
    name             text,
    pass_hash        text,
    pass_salt        text,
    password         text,
    source           text,
    source_of_breach text,
    timestamp        timestamp,
    user             text,
    user_id          text,
    PRIMARY KEY (domain, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
