#!/usr/bin/env python3
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import datetime as dt
import json

APP_DIR = Path(__file__).resolve().parent
LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
WEBHOOK_LOG = LOG_DIR / "webhook_events.jsonl"

app = FastAPI(title="Zid Ship Optimizer", version="1.0-ar")


@app.get("/health")
def health():
    return {"status": "ok", "service": "zid-ship-optimizer", "lang": "ar"}


@app.get("/", response_class=HTMLResponse)
def home():
    return (APP_DIR / "index_ar.html").read_text(encoding="utf-8")


@app.get("/oauth/callback", response_class=HTMLResponse)
def oauth_callback(code: str | None = None, state: str | None = None):
    ts = dt.datetime.now(dt.timezone.utc).isoformat()
    payload = {
        "ts": ts,
        "event": "oauth_callback",
        "code_present": bool(code),
        "state": state,
    }
    with (LOG_DIR / "oauth_callbacks.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    return """
    <html dir='rtl' lang='ar'><body style='font-family:Arial;max-width:700px;margin:40px auto'>
      <h2>✅ تم استلام الربط بنجاح</h2>
      <p>تمت معالجة رابط الرجوع (Callback) بنجاح. يمكنك العودة إلى لوحة التطبيق.</p>
    </body></html>
    """


@app.post("/webhooks/zid")
async def zid_webhook(request: Request):
    data = await request.json()
    record = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "headers": dict(request.headers),
        "body": data,
    }
    with WEBHOOK_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return JSONResponse({"ok": True})
