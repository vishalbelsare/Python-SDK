"""
wss://stream.samco.in   streaming_type: "quote"

Continuous quote stream — LTP, OHLC, OI, top bid/ask, volume.

Reference: https://docs-tradeapi.samco.in/streaming/streaming-quote-data

Install once: pip install websocket-client
Run:          python streaming_quote.py
"""

import json
import signal
import websocket

SESSION_TOKEN = "<SESSION_TOKEN>"

SUBSCRIBE = {
    "request": {
        "streaming_type": "quote",
        "data": {"symbols": [{"symbol": "532826_BSE"}]},
        "request_type": "subscribe",
        "response_format": "json",
    }
}


def on_open(ws):
    print("Connected — sending subscribe frame")
    ws.send(json.dumps(SUBSCRIBE))


def on_message(ws, msg):
    # Frame keys: sym, aPr/bPr, aSz/bSz, avgPr, c, h, l, o, oI, oIChg, ch, …
    print("Quote ::", msg)


def on_error(ws, error):
    print("WS error:", error)


def on_close(ws, code, reason):
    print("Connection closed")


if __name__ == "__main__":
    ws_app = websocket.WebSocketApp(
        "wss://stream.samco.in",
        header={"x-session-token": SESSION_TOKEN},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Unsubscribe cleanly on Ctrl-C. Always unsubscribe when streaming is
    # no longer needed.
    def _sigint(_sig, _frame):
        unsubscribe = {
            "request": {
                **SUBSCRIBE["request"],
                "request_type": "unsubscribe",
            }
        }
        try:
            ws_app.send(json.dumps(unsubscribe))
        except Exception:
            pass
        ws_app.close()

    signal.signal(signal.SIGINT, _sigint)
    ws_app.run_forever()
