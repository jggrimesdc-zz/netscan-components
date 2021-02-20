CREATE TABLE enrichments.external_iihd_data_by_count_amplified
(
    count_amplified text,
    id              uuid,
    asn             text,
    count           int,
    country_code    text,
    date            text,
    risk_id         text,
    timestamp       timestamp,
    PRIMARY KEY (count_amplified, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
