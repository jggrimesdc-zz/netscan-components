CREATE TABLE meta.scan_data_tls
(
    scan_id                        text,
    scan_user_id                   text,
    timestamp                      timestamp,
    csp_report_pass                text,
    hsts_report_pass               text,
    indicators                     text,
    ip_address                     text,
    ip_address_protocol            text,
    port_cpe                       text,
    port_name                      text,
    port_number                    text,
    port_protocol                  text,
    port_service_version           text,
    port_state                     text,
    report_pass                    text,
    report_total                   text,
    s3_raw_dump_url                text,
    set_cookie_report_pass         text,
    tls_data                       text,
    tls_validation_browser_trusted text,
    x_content_type_report_pass     text,
    xss_protection_report_pass     text,
    PRIMARY KEY ((scan_id, scan_user_id),
    timestamp
) ) WITH CLUSTERING ORDER BY (timestamp DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
