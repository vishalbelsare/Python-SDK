"""
End-to-end showcase. Loads samples/.env and runs every other sample's
function in sequence — mirrors the Java QuickStartSample and the Node
quickStart.ts.

Toggles (read from .env / shell env):
  SAMCO_RUN_PLACE_ORDER=true  -> include place_order (destructive)
  SAMCO_RUN_STREAMING=true    -> include both streaming samples
                                 (each runs ~60s then auto-shuts down).

Run: python quick_start.py
"""

import os
import sys
import threading
import time

from config import flag, load_env, require_real_credentials, section, skipped
from get_quote import get_quote
from place_order import DEFAULT_ORDER, place_order
from session_token import generate_session_token
from streaming_market_data import close_market_data_stream, stream_market_data
from streaming_quote import close_quote_stream, stream_quotes
from whoami import whoami

STREAM_DURATION_S = 60


def run_step(title: str, fn) -> None:
    section(title)
    try:
        fn()
    except Exception as exc:  # noqa: BLE001
        print(f"[{title}] failed: {type(exc).__name__}: {exc}")


def run_stream(title: str, open_fn, close_fn, duration_s: int) -> None:
    section(title)
    print(f"[{title}] streaming for {duration_s}s …")
    try:
        runner = open_fn()
    except Exception as exc:  # noqa: BLE001
        print(f"[{title}] failed: {type(exc).__name__}: {exc}")
        return

    target = getattr(runner, "start_streaming", None) or runner.run_forever
    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    time.sleep(duration_s)

    print(f"[{title}] {duration_s}s elapsed - unsubscribing and closing.")
    close_fn(runner)
    thread.join(timeout=5)


def main() -> None:
    load_env()
    api_key, api_secret = require_real_credentials()

    session_token = {"value": ""}

    def _session():
        token = generate_session_token(api_key, api_secret)
        session_token["value"] = token
        print("JWT acquired (first 24 chars):", token[:24], "…")

    run_step("1. SessionTokenSample", _session)

    if not session_token["value"]:
        print("\nAborting QuickStart: session token unavailable.")
        sys.exit(1)

    token = session_token["value"]
    # Make the JWT available to any sample that still reads it from env.
    os.environ["SAMCO_SESSION_TOKEN"] = token

    run_step("2. WhoAmISample", lambda: print(whoami(token)))
    run_step("3. QuoteSample", lambda: print(get_quote(token, "SBIN", "NSE")))

    if flag("SAMCO_RUN_PLACE_ORDER"):
        run_step("4. PlaceOrderSample", lambda: print(place_order(token, DEFAULT_ORDER)))
    else:
        skipped(
            "4. PlaceOrderSample",
            "SAMCO_RUN_PLACE_ORDER=false (destructive — set to true to enable)",
        )

    if flag("SAMCO_RUN_STREAMING"):
        quote_symbols = ["11536_NSE"]
        run_stream(
            "5. StreamingQuoteSample",
            lambda: stream_quotes(token, quote_symbols),
            lambda ws: close_quote_stream(ws, quote_symbols),
            STREAM_DURATION_S,
        )
        md_symbols = ["1594_NSE"]
        run_stream(
            "6. StreamingMarketDataSample",
            lambda: stream_market_data(token, md_symbols),
            lambda ws: close_market_data_stream(ws, md_symbols),
            STREAM_DURATION_S,
        )
    else:
        skipped("5/6. Streaming samples", "SAMCO_RUN_STREAMING=false")


if __name__ == "__main__":
    main()
