"""
GET /order/getOrderStatus?orderNumber=<ORDER_NUMBER>

Latest exchange status for a single order, looked up by the order
number returned from /order/placeOrder.

Reference: https://docs-tradeapi.samco.in/order/get-order-status

Run:
  SAMCO_ORDER_NUMBER=240207000133590 python order_status.py
"""

import json
import os
import sys
import requests

from config import BASE_URL, load_env, require_session_token


def get_order_status(session_token: str, order_number: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    params = {"orderNumber": order_number}

    r = requests.get(
        f"{BASE_URL}/order/getOrderStatus", headers=headers, params=params
    )
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Get order status failed: {payload.get('statusMessage')}")
    return payload


def main() -> None:
    load_env()
    token = require_session_token()

    order_number = os.environ.get("SAMCO_ORDER_NUMBER", "").strip()
    if not order_number:
        print(
            "SAMCO_ORDER_NUMBER is required. Set it in samples/.env or your shell, e.g.:\n"
            "  SAMCO_ORDER_NUMBER=240207000133590 python order_status.py",
            file=sys.stderr,
        )
        sys.exit(2)

    result = get_order_status(token, order_number)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
