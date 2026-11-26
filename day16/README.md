Intake stack: FastAPI app + n8n + Postgres (Docker Compose)

A small stack that runs with one command:

Service	What it is	Address on your computer
app	FastAPI webhook receiver (POST /webhook)	http://localhost:8000 (API docs at /docs)
n8n	Workflow automation	http://localhost:5678
db	Postgres with pgvector	not exposed (other services reach it as db)

The app checks a secret header (x-webhook-secret), logs the JSON it receives and replies {"ok": true}. The database is running and keeps its data, but the app does not use it yet.

Requirements
Docker Desktop, installed and running

You do not need Python installed to run the stack.

Run it
Create your .env file from the example:
cp .env.example .env
Open .env and set the values. Write them without quotes and without spaces around =:
WEBHOOK_SECRET=a-long-random-string
POSTGRES_PASSWORD=another-random-string
Start everything:
docker compose up --build

Wait until you see all three: the database is ready to accept connections, Uvicorn is running on port 8000, and n8n says the editor is accessible. 4. Open n8n at http://localhost:5678 and create the owner account (first run only).

Check that it works

In a second terminal, send a test webhook (use your own secret from .env):

curl -X POST localhost:8000/webhook \
  -H 'x-webhook-secret: a-long-random-string' \
  -H 'Content-Type: application/json' \
  -d '{"hello": "world"}'

Expected reply: {"ok":true}. The payload also appears in the app logs. A wrong or missing secret returns 401 Invalid secret.

Call the app from n8n

Add an HTTP Request node to a workflow:

Method: POST
URL: http://app:8000/webhook
Header: x-webhook-secret with your secret
Body: JSON, for example {"hello": "from n8n"}

Use app, not localhost. Inside Docker, services reach each other by service name, and localhost would mean the n8n container itself.

Stop it
docker compose down

This removes the containers but keeps your data (n8n workflows and the database) in Docker volumes. Start again with docker compose up.

Warning: docker compose down -v also deletes the volumes and all saved data. Only use it when you want a clean start.

How it is put together
.
├── Dockerfile            builds the app image
├── docker-compose.yml    defines app, n8n and db
├── .dockerignore         keeps .env, .venv and .git out of the image
├── main.py               the FastAPI app
├── requirements.txt      Python libraries
├── .env.example          variable names with placeholder values
└── .env                  your real secrets (never committed)
Secrets come from .env at start time (env_file). They are not baked into the image, because .dockerignore excludes .env.
Data lives in two named volumes, n8n_data and db_data, so it survives restarts.
Start order: app waits for the database healthcheck (pg_isready) before it starts.
Rebuild rules: change .env and restart the containers; change code, requirements.txt or the Dockerfile and run docker compose up --build.
Troubleshooting
Problem	Likely cause	Fix
Cannot connect to the Docker daemon	Docker Desktop is not running	Start it and wait until it is ready
port is already allocated	Another container or program uses 8000, 5678 or 5432	docker ps, then docker stop <name>
401 Invalid secret	Header value differs from WEBHOOK_SECRET in .env	Use the exact value, with no quotes in .env, then restart
n8n cannot reach the app	The URL uses localhost	Use http://app:8000/webhook
Compose warns that POSTGRES_PASSWORD is not set	Missing from .env	Add it and run docker compose up again
Edits to main.py have no effect	The image was not rebuilt	docker compose up --build
Notes
print is used for logging to keep the example simple.
The /webhook route compares secrets with !=. A production version would use hmac.compare_digest.