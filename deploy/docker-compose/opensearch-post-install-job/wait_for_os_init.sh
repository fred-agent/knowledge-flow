#!/usr/bin/env bash

CLUSTER_NAME=$1
TIMEOUT=120
CURL_CMD="curl https://$CLUSTER_NAME:9200/_cluster/health --insecure --silent --user admin:Azerty123_ --request GET"

cat << EOF

Waiting for OpenSearch initialization

EOF

elapsed_time=0
while output=$($CURL_CMD); [[ -z "$output" || "$output" == *"OpenSearch Security not initialized"* ]]
do
    if [ $elapsed_time -ge $TIMEOUT ]
    then
        echo "Timeout reached (${TIMEOUT}s): OpenSearch is not ready yet"
        exit 1
    fi
    printf .
    sleep 1
    (( elapsed_time++ ))
done

echo "OpenSearch is ready and secured"
