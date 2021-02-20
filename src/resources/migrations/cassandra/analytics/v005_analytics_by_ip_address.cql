CREATE TABLE analytics.by_ip_address
(
    ip_address                    text,
    timestamp                     timestamp,
    domain                        text,
    duns                          int,
    file_share_servers            text,
    high_value_personnel          text,
    insecure_systems              text,
    malware_servers               text,
    management_team               text,
    open_ports                    text,
    potentially_exploited_systems text,
    scan_user_id                  text,
    services                      text,
    PRIMARY KEY (ip_address, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
