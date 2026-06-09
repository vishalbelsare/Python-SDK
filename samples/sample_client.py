"""
SAMCO Trade API v3.2 — Sample Client

Demonstrates the recommended v3.2 flow expressed through the published
`stocknotebridge` (snapi_py_client) SDK. The bridge does not yet wrap
the v3.2 `/session/token` and `/ip/whoami` endpoints, so those two
steps fall back to raw HTTP — once obtained, the JWT is attached to
the bridge via `set_session_token()` and every other call goes through
the SDK.

Sequence:
  1. POST /session/token   → raw (replaces legacy OTP → Login chain)
  2. GET  /ip/whoami       → raw
  3. GET  /limit           → bridge.get_limits
  4. GET  /quote           → bridge.get_quote
  5. GET  /holding         → bridge.get_holding
  6. POST /order/placeOrder → bridge.place_order (MIS LIMIT — guarded)
  7. DELETE /user/logout   → bridge.logout

Run:
  pip install -r requirements.txt
  python sample_client.py
"""

import sys

from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge

from config import flag, load_env, require_real_credentials
from session_token import generate_session_token
from whoami import whoami


def log(label: str, payload) -> None:
    print(f"\n=== {label} ===")
    print(payload)


def step(label: str, fn):
    try:
        result = fn()
        log(label, result)
        return result
    except Exception as exc:  # noqa: BLE001
        print(f"\n!!! {label} failed: {type(exc).__name__}: {exc}")
        return None


def main() -> None:
    load_env()
    api_key, api_secret = require_real_credentials()

    # 1. Generate a session token (v3.2 one-step auth, raw HTTP).
    session_token = step(
        "generate_session_token (raw POST /session/token)",
        lambda: generate_session_token(api_key, api_secret),
    )
    if not session_token:
        print("Could not obtain a session token — aborting.")
        sys.exit(1)

    bridge = StocknoteAPIPythonBridge()
    bridge.set_session_token(session_token)

    # 2. Confirm the source IP the API sees (raw — bridge has no helper yet).
    step("whoami (raw GET /ip/whoami)", lambda: whoami(session_token))

    # 3. Funds & margin.
    step("bridge.get_limits", bridge.get_limits)

    # 4. Live quote.
    step(
        "bridge.get_quote (SBIN @ NSE)",
        lambda: bridge.get_quote(symbol_name="SBIN", exchange=bridge.EXCHANGE_NSE),
    )

    # 5. CNC holdings.
    step("bridge.get_holding", bridge.get_holding)

    # 6. Place an MIS limit order on SBIN well below market (stays pending).
    #    Guarded — set SAMCO_RUN_PLACE_ORDER=true in .env to enable.
    if flag("SAMCO_RUN_PLACE_ORDER"):
        step(
            "bridge.place_order (SBIN MIS LIMIT)",
            lambda: bridge.place_order(
                symbol_name="SBIN",
                exchange=bridge.EXCHANGE_NSE,
                transaction_type=bridge.TRANSACTION_TYPE_BUY,
                order_type=bridge.ORDER_TYPE_LIMIT,
                quantity="1",
                disclosed_quantity="",
                price="100",
                order_validity=bridge.VALIDITY_DAY,
                product_type=bridge.PRODUCT_MIS,
                after_market_order_flag="NO",
            ),
        )
    else:
        print(
            "\n---- bridge.place_order (skipped: SAMCO_RUN_PLACE_ORDER=false) ----"
        )

    # 7. Clean teardown.
    step("bridge.logout", bridge.logout)


if __name__ == "__main__":
    main()
