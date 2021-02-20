CREATE TABLE enrichments.external_breach_data_by_password
(
    password         text,
    id               uuid,
    domain           text,
    email            text,
    ip               text,
    name             text,
    pass_hash        text,
    pass_salt        text,
    source           text,
    source_of_breach text,
    timestamp        timestamp,
    user             text,
    user_id          text,
    PRIMARY KEY (password, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
