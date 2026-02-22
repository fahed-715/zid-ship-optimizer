# Zid Ship Optimizer — Functional v1 (Arabic-first)

## Includes
- Arabic-first landing (`/`)
- Health endpoint (`/health`)
- OAuth callback endpoint (`/oauth/callback`)
- Zid webhook receiver (`/webhooks/zid`)
- Local JSONL logs for callbacks/webhooks

## Run
```bash
cd MoneyMachine/Zid/MVPs/ZidShip_Functional_v1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8088
```

## Test
- http://127.0.0.1:8088/
- http://127.0.0.1:8088/health
- http://127.0.0.1:8088/oauth/callback?code=test&state=abc

Webhook test:
```bash
curl -X POST http://127.0.0.1:8088/webhooks/zid \
  -H 'content-type: application/json' \
  -d '{"event":"app.market.subscription.active"}'
```

## Next step to use in Zid dashboard
Replace temporary webhook/callback URLs with your production host paths:
- `/oauth/callback`
- `/webhooks/zid`
