CREATE TABLE meta.dns_data
(
    scan_id            text,
    scan_user_id       text,
    timestamp          timestamp,
    dns_record_name    text,
    alookup_data       text,
    alookup_name       text,
    alookup_status     text,
    alookup_timestamp  timestamp,
    axfr_allowed       text,
    dmarc_altered_name text,
    dmarc_data         text,
    dmarc_name         text,
    dmarc_status       text,
    dmarc_timestamp    timestamp,
    spf_data           text,
    spf_name           text,
    spf_status         text,
    spf_timestamp      timestamp,
    PRIMARY KEY ((scan_id, scan_user_id),
    timestamp,
    dns_record_name
) ) WITH CLUSTERING ORDER BY (timestamp DESC, dns_record_name DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
