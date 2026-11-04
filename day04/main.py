import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request

load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request, x_webhook_secret: str = Header(default=None)):
    if not WEBHOOK_SECRET or x_webhook_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")
    payload = await request.json()
    print("Received:", payload)
    return {"ok": True}