CREATE TABLE meta.request_input
(
    scan_id      text,
    scan_user_id text,
    company_name text,
    domain       text,
    duns         text,
    PRIMARY KEY ((scan_id, scan_user_id)
) ) WITH compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
