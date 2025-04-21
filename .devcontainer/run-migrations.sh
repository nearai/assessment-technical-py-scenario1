#!/bin/bash
set -e

source ../.env 2>/dev/null || true

# Run Alembic migrations to set up the schema and seed data
cd /workspaces/assessment-technical-py-scenario1
alembic upgrade head

echo "Migrations completed successfully!"
