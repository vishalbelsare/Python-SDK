"""
wss://stream.samco.in   streaming_type: "quote2"

Continuous market-depth stream — 5 levels of bids/asks.

Reference: https://docs-tradeapi.samco.in/streaming/streaming-market-data

Run: python streaming_market_data.py
"""

import json
import signal
import websocket

from config import STREAM_URL, load_env, require_session_token


def _build_frame(symbols: list, request_type: str) -> dict:
    return {
        "request": {
            "streaming_type": "quote2",
            "data": {"symbols": [{"symbol": s} for s in symbols]},
            "request_type": request_type,
            "response_format": "json",
        }
    }


def stream_market_data(session_token: str, symbols: list) -> websocket.WebSocketApp:
    def on_open(ws):
        print("Connected — sending subscribe frame")
        ws.send(json.dumps(_build_frame(symbols, "subscribe")))

    def on_message(_ws, msg):
        print("Market data ::", msg)

    def on_error(_ws, error):
        print("WS error:", error)

    def on_close(_ws, _code, _reason):
        print("Connection closed")

    return websocket.WebSocketApp(
        STREAM_URL,
        header={"x-session-token": session_token},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )


def close_market_data_stream(ws: websocket.WebSocketApp, symbols: list) -> None:
    try:
        ws.send(json.dumps(_build_frame(symbols, "unsubscribe")))
    except Exception:
        pass
    ws.close()


def main() -> None:
    load_env()
    token = require_session_token()

    symbols = ["3880_NSE", "30125_NSE"]
    ws_app = stream_market_data(token, symbols)

    def _sigint(_sig, _frame):
        close_market_data_stream(ws_app, symbols)

    signal.signal(signal.SIGINT, _sigint)
    ws_app.run_forever()


if __name__ == "__main__":
    main()
