#!/bin/bash
set -e

source ../.env 2>/dev/null || true

# Run database migrations using Python
# This is a placeholder - replace with the actual migration command for your project
# Examples:
# - For Alembic: alembic upgrade head
# - For Django: python manage.py migrate
# - For SQLAlchemy: python -m your_package.db.migrations

cd /workspace
python -m agent_discovery.lib.db migrate

echo "Migrations completed successfully!"
