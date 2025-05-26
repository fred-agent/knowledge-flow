#!/usr/bin/env bash

CERTS_DIR=$1
COUNTRY="FR"
STATE="France"
LOCATION="Rennes"
ORGANIZATION="Dev"

function generate_root_cert
{
    openssl genpkey -algorithm RSA -out ca.key -pkeyopt rsa_keygen_bits:4096
    openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/CN=OpenSearch-CA"
}

function generate_cert
{
    local NAME=$1
    local COMMON_NAME=$2
    openssl genpkey -algorithm RSA -out ${NAME}.key -pkeyopt rsa_keygen_bits:4096
    openssl req -new -key ${NAME}.key -out ${NAME}.csr -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/CN=${COMMON_NAME}"
    openssl x509 -req -in ${NAME}.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ${NAME}.crt -days 365 -sha256
    cat ${NAME}.crt ${NAME}.key > ${NAME}.pem
}

cd $CERTS_DIR

generate_root_cert
generate_cert "transport" "node"
generate_cert "admin" "admin"
generate_cert "rest" "rest"
