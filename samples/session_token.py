"""
POST /session/token

Direct, headless authentication using your OAuth app's AES-encrypted
API Key + API Secret. Captures the returned JWT and reuses it as the
`x-session-token` header on a follow-up call.

Reference: https://docs-tradeapi.samco.in/session/generate-token

Install once: pip install requests
Run:          python session_token.py
"""

import json
import requests

BASE_URL = "https://tradeapi.samco.in"


def generate_session_token(api_key: str, api_secret: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = {"apiKey": api_key, "apiSecret": api_secret}

    r = requests.post(
        f"{BASE_URL}/session/token",
        data=json.dumps(body),
        headers=headers,
    )
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Session token failed: {payload.get('statusMessage')}")
    return payload


def get_holdings(session_token: str) -> dict:
    # Reuse the JWT as `x-session-token` on subsequent Trade API calls.
    headers = {
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    return requests.get(f"{BASE_URL}/holding/getHolding", headers=headers).json()


if __name__ == "__main__":
    session = generate_session_token(
        "<AES_ENCRYPTED_API_KEY>",
        "<AES_ENCRYPTED_API_SECRET>",
    )

    print("accountID:    ", session["accountID"])
    print("srcIp:        ", session["srcIp"])
    print("primaryIp:    ", session["primaryIp"])
    print("secondaryIp:  ", session["secondaryIp"])
    print("sessionToken: ", session["sessionToken"][:24], "...")

    # The token is valid until 08:00 IST the next day.
    holdings = get_holdings(session["sessionToken"])
    print("Holdings:", holdings)
