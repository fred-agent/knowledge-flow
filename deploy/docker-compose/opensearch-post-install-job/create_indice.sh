#!/usr/bin/env bash

cd $(dirname $0)

cat << EOF

Create first indice

EOF

ret=0

curl https://bidgpt-opensearch:9200/bidgpt-dev-metadata \
    --insecure \
    --silent \
    --user admin:Azerty123_ \
    --request PUT \
    --data-binary @mapping-metadata.json \
    --header "Content-Type: application/json" || (( ret+=$? ))

curl https://bidgpt-opensearch:9200/bidgpt-dev-embeddings \
    --insecure \
    --silent \
    --user admin:Azerty123_ \
    --request PUT \
    --data-binary @mapping-vector.json \
    --header "Content-Type: application/json" || (( ret+=$? ))

curl https://bidgpt-opensearch:9200/bidgpt-dev-chat-interactions \
    --insecure \
    --silent \
    --user admin:Azerty123_ \
    --request PUT \
    --data-binary @mapping-chat.json \
    --header "Content-Type: application/json" || (( ret+=$? ))

curl https://bidgpt-opensearch:9200/bidgpt-dev-active-sessions \
    --insecure \
    --silent \
    --user admin:Azerty123_ \
    --request PUT \
    --data-binary @mapping-sessions.json \
    --header "Content-Type: application/json" || (( ret+=$? ))

echo

exit $ret
