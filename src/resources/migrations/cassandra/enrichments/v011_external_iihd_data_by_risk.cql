CREATE TABLE enrichments.external_iihd_data_by_risk
(
    risk_id         text,
    id              uuid,
    asn             text,
    count           int,
    count_amplified text,
    country_code    text,
    date            text,
    timestamp       timestamp,
    PRIMARY KEY (risk_id, id)
) WITH CLUSTERING ORDER BY (id DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
