#!/bin/bash


set -e

POSTGRES="psql --username ${POSTGRES_USER}"

for dbname in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
    echo "Creating database: ${dbname}"
    $POSTGRES <<-EOSQL
        CREATE DATABASE ${dbname} OWNER ${POSTGRES_USER};
EOSQL
done

echo "All databases created successfully"

