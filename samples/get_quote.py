"""
GET /quote/getQuote

Quote details for an equity / derivative scrip — LTP, previous close,
OHLC, top bids/asks, circuit limits, etc.

Reference: https://docs-tradeapi.samco.in/quote/get-quote

Install once: pip install requests
Run:          python get_quote.py
"""

import requests

BASE_URL = "https://tradeapi.samco.in"


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
    return payload["quoteDetails"]


if __name__ == "__main__":
    SESSION_TOKEN = "<SESSION_TOKEN>"

    quote = get_quote(SESSION_TOKEN, "ASIANPAINT24APR2760PE", "NFO")

    print("symbol:        ", quote["tradingSymbol"])
    print("LTP:           ", quote["lastTradedPrice"])
    print("previousClose: ", quote["previousClose"])
    print(
        "change:        ",
        quote["changeValue"],
        f"({quote['changePercentage']}%)",
    )
    print(
        "OHLC:          ",
        quote["openValue"],
        quote["highValue"],
        quote["lowValue"],
        quote["closeValue"],
    )

    best_bid = (quote.get("bestBids") or [{}])[0]
    best_ask = (quote.get("bestAsks") or [{}])[0]
    print("best bid:      ", best_bid.get("price"), "x", best_bid.get("quantity"))
    print("best ask:      ", best_ask.get("price"), "x", best_ask.get("quantity"))
