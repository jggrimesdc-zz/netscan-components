CREATE TABLE enrichments.external_iihd_data_by_country
(
    country_code    text,
    id              uuid,
    asn             text,
    count           int,
    count_amplified text,
    date            text,
    risk_id         text,
    timestamp       timestamp,
    PRIMARY KEY (country_code, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
