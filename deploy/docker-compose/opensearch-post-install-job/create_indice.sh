#!/usr/bin/env bash

CLUSTER_NAME=$1
INDEX_NAME=$2

cd $(dirname $0)

cat << EOF

Create first indice

EOF

if ! curl -v https://$CLUSTER_NAME:9200/$INDEX_NAME \
    --fail \
    --insecure \
    --silent \
    --user admin:Azerty123_
then
    curl -v https://$CLUSTER_NAME:9200/$INDEX_NAME \
        --insecure \
        --silent \
        --user admin:Azerty123_ \
        --request PUT \
        --data-binary @mapping.json \
        --header "Content-Type: application/json"
fi