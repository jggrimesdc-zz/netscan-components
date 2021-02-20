#!/usr/bin/env bash

ACCOUNT_ID="wcaas-crud-prod"
USER_ID="12345"
CLUSTER_ID="1001"

# QA
#BASE_URL="http://internal-ab964cfaba50c4b17b4b4865903c0aee-1757907119.us-east-2.elb.amazonaws.com:8080"
# DEV
BASE_URL="http://internal-a62e497fda8374d1383558fb72b4f6b9-2073955393.us-east-2.elb.amazonaws.com:8080"
ENDPOINT="api/clusters/${CLUSTER_ID}/keyspaces"

declare -a KEYSPACES=("mgmt" "dqm" "meta" "status" "analytics" "score")

for KEYSPACE_NAME in "${KEYSPACES[@]}"; do
  echo "Deleting keyspace ${KEYSPACE_NAME}..."
  curl -X DELETE "${BASE_URL}/${ENDPOINT}/${KEYSPACE_NAME}" \
    -H "accept: */*" \
    -H "X-netscan-CustomerAccountId: ${ACCOUNT_ID}" \
    -H "X-netscan-UserId: ${USER_ID}"
  echo "Keyspace ${KEYSPACE_NAME} deleted."

  echo "Creating keyspace ${KEYSPACE_NAME}..."
  curl -X POST "${BASE_URL}/${ENDPOINT}" \
    -H "accept: */*" \
    -H "X-netscan-CustomerAccountId: ${ACCOUNT_ID}" \
    -H "X-netscan-UserId: ${USER_ID}" \
    -H "Content-Type: application/json" \
    -d "{ \"name\": \"${KEYSPACE_NAME}\", \"replicationFactorMainDatacenter\": 3, \"replicationFactorSecondDatacenter\": 1}"

  echo ""
  echo "Keyspace ${KEYSPACE_NAME} created."

  echo "Ensure Filtering Allowed on Cluster..."
  curl -X PUT "${BASE_URL}/api/clusters/${CLUSTER_ID}/filter" \
    -H "accept: */*" \
    -H "X-netscan-CustomerAccountId: ${ACCOUNT_ID}" \
    -H "X-netscan-UserId: ${USER_ID}" \
    -H "Content-Type: application/json" \
    -d "{ \"allowFiltering\": true}"

  echo "Building tables in ${KEYSPACE_NAME}..."
  sh build_tables_in_keyspace.sh "${KEYSPACE_NAME}" "${CLUSTER_ID}" "${ACCOUNT_ID}"
  echo "Tables in ${KEYSPACE_NAME} created."
  echo ""
done
