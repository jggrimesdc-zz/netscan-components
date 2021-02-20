DROP TABLE enrichments.external_iihd_by_risk;

CREATE TABLE enrichments.external_iihd_by_risk
(
    COUNTRY_CODE              text,
    ID                        uuid,
    TIMESTAMP                 timestamp,
    DATE                      text,
    ASN                       text,
    ASN_ID                    text,
    COUNT                     int,
    COUNT_AMPLIFIED           text,
    RISK_TITLE                text,
    RISK_ID                   text,
    RISK_SLUG                 text,
    RISK_IS_ARCHIVED          boolean,
    RISK_TAXONOMY             text,
    RISK_MEASUREMENT_UNITS    text,
    RISK_AMPLIFICATION_FACTOR text,
    RISK_DESCRIPTION          text,

    PRIMARY KEY (RISK_TITLE, ID)
) WITH CLUSTERING ORDER BY (ID DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
