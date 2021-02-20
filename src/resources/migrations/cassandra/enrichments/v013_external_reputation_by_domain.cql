DROP TABLE enrichments.external_reputation_data_by_domain;

CREATE TABLE enrichments.external_reputation_by_domain
(
    ID                   uuid,
    EFFECTIVE_FROM       text,
    LAST_SEEN            text,
    IP                   text,
    PORT                 text,
    SSL_SHA              text,
    URL                  text,
    DOMAIN               text,
    STATUS               text,
    THREAT               text,
    TAGS                 text,
    SOURCE_OF_REPUTATION text,
    REPORTED_BY          text,
    TIMESTAMP            timestamp,
    COUNTRY              text,
    CITY                 text,
    LAT                  text,
    LONG                 text,
    THREAT_TYPE          text,
    SOURCE_SYSTEM_ID     text,
    SOURCE_DETAIL_URL    text,
    VERIFIED             text,
    VERIFICATION_TIME    text,
    ONLINE               text,
    TARGET               text,

    PRIMARY KEY (DOMAIN, TIMESTAMP)

) WITH CLUSTERING ORDER BY (TIMESTAMP DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
