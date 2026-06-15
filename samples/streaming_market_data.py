"""
wss://stream.samco.in   streaming_type: "quote2"

Continuous market-depth stream — 5 levels of bids/asks.

Uses StocknoteAPIPythonBridge (stocknotebridge >= 3.2.2) so the v3.2
streamer fix (TRD-1467) is exercised.

Reference: https://docs-tradeapi.samco.in/streaming/streaming-market-data

Run: python streaming_market_data.py
"""

import signal

from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge

from config import load_env, require_session_token


def stream_market_data(session_token: str, symbols: list) -> StocknoteAPIPythonBridge:
    bridge = StocknoteAPIPythonBridge()
    bridge.set_session_token(session_token)
    bridge.set_streaming_data(symbols, StocknoteAPIPythonBridge.STREAMING_TYPE_MARKET_DEPTH)
    return bridge


def close_market_data_stream(bridge: StocknoteAPIPythonBridge, symbols: list) -> None:
    try:
        bridge.unsubscribe_market_data(symbols)
    except Exception:
        pass
    try:
        bridge.ws.close()
    except Exception:
        pass


def main() -> None:
    load_env()
    token = require_session_token()

    symbols = ["3880_NSE", "30125_NSE"]
    bridge = stream_market_data(token, symbols)

    def _sigint(_sig, _frame):
        close_market_data_stream(bridge, symbols)

    signal.signal(signal.SIGINT, _sigint)
    bridge.start_streaming()


if __name__ == "__main__":
    main()
