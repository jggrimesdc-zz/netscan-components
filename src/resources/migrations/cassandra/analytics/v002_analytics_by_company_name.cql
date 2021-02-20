CREATE TABLE analytics.by_company_name
(
    company_name           text,
    timestamp              timestamp,
    company_info           text,
    discoverable_code_info text,
    duns                   int,
    email_address          text,
    ip_address             text,
    personnel_code_repo    text,
    phys_op_loc            text,
    public_doc             text,
    public_metadata        text,
    scan_user_id           text,
    PRIMARY KEY (company_name, timestamp)
)
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
