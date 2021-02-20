CREATE TABLE enrichments.external_iihd_data_by_count
(
    count           int,
    id              uuid,
    asn             text,
    count_amplified text,
    country_code    text,
    date            text,
    risk_id         text,
    timestamp       timestamp,
    PRIMARY KEY (count, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
