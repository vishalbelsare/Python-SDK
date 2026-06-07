"""
POST /order/placeOrder

LIMIT order variant (orderType: "L", price required).

⚠ Live trading endpoint. Samco does not provide a sandbox. Successful
calls affect real positions and balances — review every field before
running.

Reference: https://docs-tradeapi.samco.in/order/place-order

Install once: pip install requests
Run:          python place_order.py
"""

import json
import requests

BASE_URL = "https://tradeapi.samco.in"


def place_limit_order(session_token: str, body: dict) -> dict:
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


if __name__ == "__main__":
    SESSION_TOKEN = "<SESSION_TOKEN>"

    limit_order = {
        "symbolName": "IDEA",
        "exchange": "NSE",
        "transactionType": "BUY",
        "orderType": "L",                # LIMIT
        "quantity": "1",
        "disclosedQuantity": "1",
        "orderValidity": "DAY",          # or "IOC"
        "productType": "CNC",            # or "MIS" / "NRML"
        "afterMarketOrderFlag": "NO",
        "price": "13.40",                # required for L
    }

    result = place_limit_order(SESSION_TOKEN, limit_order)

    print("orderNumber:         ", result["orderNumber"])
    print("exchangeOrderStatus: ", result["exchangeOrderStatus"])
    print("tradingSymbol:       ", result["orderDetails"]["tradingSymbol"])
    print("orderPrice:          ", result["orderDetails"]["orderPrice"])
    print("orderTime:           ", result["orderDetails"]["orderTime"])
