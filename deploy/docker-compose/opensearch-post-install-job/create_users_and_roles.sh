#!/usr/bin/env bash

CLUSTER_NAME=$1

while ! /usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh \
    --accept-red-cluster \
    --configdir /usr/share/opensearch/config/opensearch-security/ \
    --ignore-clustername \
    --disable-host-name-verification \
    --hostname $CLUSTER_NAME \
    --port 9200 \
    -cacert /usr/share/opensearch/config/certs/ca.crt \
    -cert /usr/share/opensearch/config/certs/admin.crt \
    -key /usr/share/opensearch/config/certs/admin.key
do
    sleep 5
done
