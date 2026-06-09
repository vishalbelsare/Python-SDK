"""
GET /order/orderBook

All orders placed during the current trading day with their latest
exchange status.

Reference: https://docs-tradeapi.samco.in/order/order-book

Run: python order_book.py
"""

import json
import requests

from config import BASE_URL, load_env, require_session_token


def get_order_book(session_token: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    r = requests.get(f"{BASE_URL}/order/orderBook", headers=headers)
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Get order book failed: {payload.get('statusMessage')}")
    return payload


def main() -> None:
    load_env()
    token = require_session_token()

    result = get_order_book(token)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
