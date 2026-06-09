"""
POST /order/placeOrder

LIMIT order variant (orderType: "L", price required).

⚠ Live trading endpoint. Samco does not provide a sandbox. Successful
calls affect real positions and balances — review every field before
running.

Reference: https://docs-tradeapi.samco.in/order/place-order

Run: python place_order.py
"""

import json
import requests

from config import BASE_URL, load_env, require_session_token


def place_order(session_token: str, body: dict) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    r = requests.post(
        f"{BASE_URL}/order/placeOrder",
        data=json.dumps(body),
        headers=headers,
    )
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Place order failed: {payload.get('statusMessage')}")
    return payload


DEFAULT_ORDER = {
    "symbolName": "IDEA",
    "exchange": "NSE",
    "transactionType": "BUY",
    "orderType": "L",
    "quantity": "1",
    "disclosedQuantity": "1",
    "orderValidity": "DAY",
    "productType": "CNC",
    "afterMarketOrderFlag": "NO",
    "price": "13.40",
}


def main() -> None:
    load_env()
    token = require_session_token()

    result = place_order(token, DEFAULT_ORDER)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
