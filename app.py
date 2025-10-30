import os
from fastapi import FastAPI, Request
import httpx

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI()

@app.get("/")
async def health():
    return {"ok": True}

async def send_message(chat_id: int, text: str):
    if not BOT_TOKEN:
        return
    async with httpx.AsyncClient(timeout=10) as cx:
        await cx.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.post("/telegram/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    msg = data.get("message") or data.get("edited_message")
    if not msg:
        return {"ok": True}
    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()

    if text.lower().startswith("/start"):
        await send_message(chat_id, "✅ Bot is live.\nUse /status")
    elif text.lower().startswith("/status"):
        await send_message(chat_id, "🟢 Monitoring service is online (webhook).")
    else:
        await send_message(chat_id, "Try /start or /status")

    return {"ok": True}
