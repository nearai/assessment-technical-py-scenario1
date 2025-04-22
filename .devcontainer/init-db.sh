#!/bin/bash
set -e

# This script is run when the PostgreSQL container is started for the first time.
# It initializes the database for the Python application.

# Create the database if it doesn't exist
# Check for .env file in /workspace or ../ and source it
if [ -f /workspace/.env ]; then
    source /workspace/.env
elif [ -f ../.env ]; then
    source ../.env
elif [ -f ./.env ]; then
    source ./.env
else
    echo "No .env file found in /workspace or ../"
    exit 1
fi
psql -v ON_ERROR_STOP=1 -h "$DB_HOST" -p "$DB_PORT" --username "$DB_USER" <<-EOSQL
    CREATE DATABASE $DB_NAME;

    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL