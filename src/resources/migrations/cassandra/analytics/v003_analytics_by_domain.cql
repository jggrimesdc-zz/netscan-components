CREATE TABLE analytics.by_domain
(
    domain_name                   text,
    timestamp                     timestamp,
    company_info                  text,
    dkim                          text,
    dmarc                         text,
    duns                          int,
    email_address                 text,
    file_share_servers            text,
    insecure_systems              text,
    ip_address                    text,
    malware_servers               text,
    open_ports                    text,
    potentially_exploited_systems text,
    scan_user_id                  text,
    spf                           text,
    PRIMARY KEY (domain_name, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
