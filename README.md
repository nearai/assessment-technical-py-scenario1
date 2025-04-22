# Instructions for Candidates
1. Fork this repository into a new PRIVATE repository in your own GitHub account.
2. A postgres DB is recommended
3. Run the app

## assessment-technical-py-scenario1
Template repo for technical assessments in Python, scenario 1.

## Getting Started

 * Option 1. This project has a devcontainer configuration
 * Option 2. Or the .devcontainer/docker-compose.yml can be run directly
 * Option 3. Open in codespaces https://codespaces.new/nearai/assessment-technical-py-scenario1
 * Option 4. Run it step by step as detailed below

### Running step by step

1. You will need to run Postgres locally or with .devcontainer/docker-compose.yml

1. Set up a virtual environment and Install dependencies:

```bash
uv sync
source ./.venv/bin/activate
```

2. Set up environment variables in a `.env` file:

```
DB_USER=postgres
DB_HOST=localhost
DB_NAME=agent_discovery
DB_PASSWORD=postgres
DB_PORT=5432
```

## DB helper scripts
The scripts `.devcontainer/init-db.sh` and `.devcontainer/run-migrations.sh` 

## Database Migrations

This project uses Alembic for database migrations. To run the migrations:

1. Make sure your database is running and the environment variables are set correctly in your `.env` file.

2. Make sure you have an `agent_discovery` database created in your Postgres instance.

3. Run the migrations:

```bash
alembic upgrade head
```

This will create the necessary tables and seed the initial data.

This script will:
1. Run the Alembic migrations
2. Test the database connection
3. Verify that the tables exist
4. Check that the data was seeded correctly

## Running the Application

Start the FastAPI server:

```bash
python run.py
```

The server will start on http://localhost:8000

You can also access the interactive API documentation at http://localhost:8000/docs
