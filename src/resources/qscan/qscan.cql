CREATE
KEYSPACE IF NOT EXISTS "qscan"
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE
"qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_company_name"
(
    "axfr"
    boolean,
    "company_name"
    text,
    "dmarc"
    boolean,
    "ip_addresses"
    list<
    text>,
    "ports"
    list<
    int>,
    "protocols"
    list<
    text>,
    "services"
    list<
    text>,
    "spf"
    boolean,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "company_name",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_company_protocol"
(
    "company_name"
    text,
    "domains"
    text,
    "ports"
    list<
    int>,
    "protocol"
    text,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "company_name",
    "timestamp",
    "protocol"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC, "protocol" ASC);

CREATE TABLE IF NOT EXISTS "qscan"."by_domain_name"
(
    "axfr"
    boolean,
    "dmarc"
    boolean,
    "domain_name"
    text,
    "ip_addresses"
    tuple<
    text>,
    "ports"
    list<
    int>,
    "spf"
    boolean,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "domain_name",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_ip_port"
(
    "headers"
    text,
    "ip"
    text,
    "port"
    text,
    "service"
    text,
    "timestamp"
    timestamp,
    PRIMARY
    KEY (
(
    "ip",
    "port"
), "timestamp")
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_ipaddress"
(
    "company_name"
    text,
    "cpe"
    text,
    "domain_name"
    text,
    "ip_address"
    text,
    "ports"
    list<
    text>,
    "services"
    list<
    text>,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "ip_address",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_port"
(
    "headers"
    text,
    "port"
    text,
    "service"
    text,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "port",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_protocol"
(
    "company_name"
    text,
    "domains"
    text,
    "ports"
    list<
    int>,
    "protocol"
    text,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "protocol",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_service_name"
(
    "company_name"
    text,
    "ports"
    list<
    text>,
    "service"
    text,
    "timestamp"
    timestamp,
    PRIMARY
    KEY
(
    "service",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."company_scores"
(
    "ca"
    list<
    text>,
    "certificate_data"
    text,
    "company_name"
    text,
    "cpe"
    text,
    "dmarc"
    text,
    "high_impact_weight"
    text,
    "low_impact_weight"
    text,
    "medium_impact_weight"
    text,
    "number_ip_addr"
    int,
    "open_ports_non_standard"
    list<
    text>,
    "open_ports_standard"
    list<
    text>,
    "spf"
    text,
    "timestamp"
    timestamp,
    "total_core"
    text,
    PRIMARY
    KEY
(
    "company_name",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."domain_company"
(
    "company_name"
    text,
    "domain_name"
    text,
    "port"
    list<
    int>,
    "timestamp"
    timestamp,
    PRIMARY
    KEY (
(
    "domain_name",
    "company_name"
), "timestamp")
    )
    WITH bloom_filter_fp_chance = 0.01
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy','max_threshold':'32','min_threshold':'4'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."domain_scores"
(
    "ca"
    list<
    text>,
    "certificate_data"
    text,
    "cpe"
    text,
    "dmarc"
    text,
    "domain_name"
    text,
    "high_impact_weight"
    text,
    "low_impact_weight"
    text,
    "medium_impact_weight"
    text,
    "number_ip_addr"
    int,
    "open_ports_non_standard"
    list<
    text>,
    "open_ports_standard"
    list<
    text>,
    "spf"
    text,
    "timestamp"
    timestamp,
    "total_score"
    text,
    PRIMARY
    KEY
(
    "domain_name",
    "timestamp"
)
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."scanid_domain"
(
    "certificate_data"
    text,
    "domain_name"
    text,
    "number_ips"
    int,
    "number_std_ports"
    int,
    "number_websites"
    int,
    "port_cpe"
    text,
    "scan_id"
    text,
    "timestamp"
    timestamp,
    "valid_websites"
    int,
    PRIMARY
    KEY (
(
    "scan_id",
    "domain_name"
), "timestamp")
    )
    WITH bloom_filter_fp_chance = 0.1
        AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
        AND dclocal_read_repair_chance = 0.1
        AND default_time_to_live = 0
        AND gc_grace_seconds = 864000
        AND memtable_flush_period_in_ms = 0
        AND min_index_interval = 128
        AND max_index_interval = 2048
        AND read_repair_chance = 0
        AND speculative_retry = '99PERCENTILE'
        AND crc_check_chance = 1
        AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
        AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
        AND CLUSTERING ORDER BY ("timestamp" DESC);
