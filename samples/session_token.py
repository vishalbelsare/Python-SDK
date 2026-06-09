"""
POST /session/token

Direct, headless authentication using your OAuth app's AES-encrypted
API Key + API Secret. Captures the returned JWT and reuses it as the
`x-session-token` header on a follow-up call.

Reference: https://docs-tradeapi.samco.in/session/generate-token

Run: python session_token.py
"""

import json
import requests

from config import BASE_URL, load_env, require_real_credentials


def generate_session_token(api_key: str, api_secret: str) -> str:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    body = {"apiKey": api_key, "apiSecret": api_secret}

    r = requests.post(
        f"{BASE_URL}/session/token",
        data=json.dumps(body),
        headers=headers,
    )
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Session token failed: {payload.get('statusMessage')}")
    return payload["sessionToken"]


def main() -> None:
    load_env()
    api_key, api_secret = require_real_credentials()

    token = generate_session_token(api_key, api_secret)

    print("JWT acquired (first 24 chars):", token[:24], "…")
    print()
    print("Paste this value into SAMCO_SESSION_TOKEN in samples/.env.")
    print("The token is valid until 08:00 IST the next day.")


if __name__ == "__main__":
    main()
