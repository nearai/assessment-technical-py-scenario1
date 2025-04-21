# Instructions for Candidates
1. Fork this repository into a new PRIVATE repository in your own GitHub account.
2. A postgres DB is recommended
3. Run the app

## assessment-technical-py-scenario1
Template repo for technical assessments in Python, scenario 1.

## Getting Started

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

## Running the Application

Start the FastAPI server:

```bash
python run.py
```

The server will start on http://localhost:8000

You can also access the interactive API documentation at http://localhost:8000/docs