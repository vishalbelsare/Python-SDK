"""
wss://stream.samco.in   streaming_type: "quote"

Continuous quote stream — LTP, OHLC, OI, top bid/ask, volume.

Uses StocknoteAPIPythonBridge (stocknotebridge >= 3.2.2) so the v3.2
streamer fix (TRD-1467) is exercised.

Reference: https://docs-tradeapi.samco.in/streaming/streaming-quote-data

Run: python streaming_quote.py
"""

import signal

from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge

from config import load_env, require_session_token


def stream_quotes(session_token: str, symbols: list) -> StocknoteAPIPythonBridge:
    """Configure a SnapiBridge for a quote stream subscribing to `symbols`.

    The caller drives the loop with `bridge.start_streaming()` (e.g. in a
    thread) and calls `close_quote_stream(bridge, symbols)` when done.
    """
    bridge = StocknoteAPIPythonBridge()
    bridge.set_session_token(session_token)
    bridge.set_streaming_data(symbols, StocknoteAPIPythonBridge.STREAMING_TYPE_QUOTE)
    return bridge


def close_quote_stream(bridge: StocknoteAPIPythonBridge, symbols: list) -> None:
    try:
        bridge.unsubscribe_quote(symbols)
    except Exception:
        pass
    try:
        bridge.ws.close()
    except Exception:
        pass


def main() -> None:
    load_env()
    token = require_session_token()

    symbols = ["532826_BSE"]
    bridge = stream_quotes(token, symbols)

    def _sigint(_sig, _frame):
        close_quote_stream(bridge, symbols)

    signal.signal(signal.SIGINT, _sigint)
    bridge.start_streaming()


if __name__ == "__main__":
    main()
