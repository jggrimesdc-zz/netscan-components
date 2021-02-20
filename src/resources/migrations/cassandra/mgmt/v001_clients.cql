CREATE TABLE mgmt.clients
(
    customer_account_id text,
    user_id             text,
    onboard_time        timestamp,
    scan_user_id        text,
    status              text,
    PRIMARY KEY ((customer_account_id, user_id),
    onboard_time
) ) WITH CLUSTERING ORDER BY (onboard_time DESC)
   AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};

