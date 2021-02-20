CREATE TABLE enrichments.external_iihd_data_by_date
(
    date            text,
    id              uuid,
    asn             text,
    count           int,
    count_amplified text,
    country_code    text,
    risk_id         text,
    timestamp       timestamp,
    PRIMARY KEY (date, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
