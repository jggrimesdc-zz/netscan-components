CREATE TABLE meta.scheduled_scans
(
    schedule_id         text,
    scan_user_id        text,
    customer_account_id text,
    user_id             text,
    recurrence          text, -- daily, weekly, monthly, quarterly
    company_name        text,
    domains             text,
    duns                text,
    last_scheduled_run  timestamp,
    next_scheduled_run  timestamp,
    created_on          timestamp,
    PRIMARY KEY (schedule_id)
)
    WITH compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'};

-- CREATE INDEX idx_scheduled_scans_schedule_id ON meta.scheduled_scans (scan_user_id, recurrence);
