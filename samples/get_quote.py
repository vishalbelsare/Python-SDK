"""
GET /quote/getQuote

Quote details for an equity / derivative scrip — LTP, previous close,
OHLC, top bids/asks, circuit limits, etc.

Reference: https://docs-tradeapi.samco.in/quote/get-quote

Run: python get_quote.py
"""

import json
import os
import requests

from config import BASE_URL, load_env, require_session_token


def get_quote(session_token: str, symbol_name: str, exchange: str = "NSE") -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    params = {"symbolName": symbol_name, "exchange": exchange}

    r = requests.get(f"{BASE_URL}/quote/getQuote", headers=headers, params=params)
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Get quote failed: {payload.get('statusMessage')}")
    return payload


def main() -> None:
    load_env()
    token = require_session_token()

    symbol = os.environ.get("SAMCO_QUOTE_SYMBOL", "SBIN")
    exchange = os.environ.get("SAMCO_QUOTE_EXCHANGE", "NSE")

    result = get_quote(token, symbol, exchange)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
