# Intake stack (FastAPI app + n8n + Postgres)

## Run it
1. Install Docker Desktop and start it.
2. Copy `.env.example` to `.env` and fill in the values (no quotes).
3. Start everything:
   ```
   docker compose up --build
   ```
4. Open n8n at http://localhost:5678 and the app at http://localhost:8000/docs.
5. In n8n, call the app at `http://app:8000/webhook` with the header `x-webhook-secret`.

## Stop it
```
docker compose down
```
Your data stays in Docker volumes. Do not use `down -v` unless you want to erase it.