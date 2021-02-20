#!/usr/bin/env bash

KEYSPACE_NAME=$1
CLUSTER_ID=$2
ACCOUNT_ID=$3
USER_ID="12345"

# QA
#BASE_URL="http://internal-ab964cfaba50c4b17b4b4865903c0aee-1757907119.us-east-2.elb.amazonaws.com:8080"
# DEV
BASE_URL="http://internal-a62e497fda8374d1383558fb72b4f6b9-2073955393.us-east-2.elb.amazonaws.com:8080"
ENDPOINT="api/clusters/${CLUSTER_ID}/keyspaces/${KEYSPACE_NAME}/tables"

for f in ./config/"${KEYSPACE_NAME}"/*.json; do
  filename=$(basename -- "$f")
  TABLE_NAME="${filename%.*}"
  if [[ ! -f "$f" ]]; then
    echo "Keyspace does not exist, aborting process."
    exit 1
  fi
  CREATE_JSON_DATA=$(cat "$f")

  echo "Deleting table ${TABLE_NAME}..."
  curl -X DELETE "${BASE_URL}/${ENDPOINT}/${TABLE_NAME}" \
    -H "accept: */*" \
    -H "X-netscan-CustomerAccountId: ${ACCOUNT_ID}" \
    -H "X-netscan-UserId: ${USER_ID}"
  echo "Table ${TABLE_NAME} deleted."

  echo "Creating table ${TABLE_NAME}..."
  curl -X POST "${BASE_URL}/${ENDPOINT}" \
    -H "accept: */*" \
    -H "X-netscan-CustomerAccountId: ${ACCOUNT_ID}" \
    -H "X-netscan-UserId: ${USER_ID}" \
    -H "Content-Type: application/json" \
    -d "${CREATE_JSON_DATA}"
  echo "Table ${TABLE_NAME} created."
done
