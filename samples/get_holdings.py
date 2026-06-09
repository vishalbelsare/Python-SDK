"""
GET /holding/getHoldings

CNC holdings (demat positions) for the authenticated account.

Reference: https://docs-tradeapi.samco.in/holdings/get-holdings

Run: python get_holdings.py
"""

import json
import requests

from config import BASE_URL, load_env, require_session_token


def get_holdings(session_token: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    r = requests.get(f"{BASE_URL}/holding/getHoldings", headers=headers)
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Get holdings failed: {payload.get('statusMessage')}")
    return payload


def main() -> None:
    load_env()
    token = require_session_token()

    result = get_holdings(token)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
