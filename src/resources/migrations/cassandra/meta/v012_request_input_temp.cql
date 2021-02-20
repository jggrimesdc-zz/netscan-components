CREATE TABLE meta.request_input_temp
(
    scan_id      text,
    company_name text,
    domain       text,
    duns         text,
    scan_user_id text,
    PRIMARY KEY ((scan_id)
) ) WITH compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};
