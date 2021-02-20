CREATE TABLE enrichments.external_breach_data_by_email
(
    email            text,
    id               uuid,
    domain           text,
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
    PRIMARY KEY (email, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
