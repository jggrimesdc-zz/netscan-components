#!/bin/bash
set -e
IPS=$(node cassandra-pod-ips.js --max=3)
cassandra-migrate --hosts $IPS --assume-yes --config-file analytics/analytics.yaml migrate
cassandra-migrate --hosts $IPS --assume-yes --config-file dqm/dqm.yaml migrate
cassandra-migrate --hosts $IPS --assume-yes --config-file enrichments/enrichments.yaml migrate
cassandra-migrate --hosts $IPS --assume-yes --config-file meta/meta.yaml migrate
cassandra-migrate --hosts $IPS --assume-yes --config-file mgmt/mgmt.yaml migrate
cassandra-migrate --hosts $IPS --assume-yes --config-file score/score.yaml migrate
cassandra-migrate --hosts $IPS --assume-yes --config-file status/status.yaml migrate
