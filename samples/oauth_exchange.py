"""
OAuth 2.1 Authorization-Code Flow

1. Exchange the auth code (from the callback URL ?code=...) at POST /oauth/token
2. Use access_token as `x-session-token` to call GET /holding/getHolding
3. Refresh the access_token at POST /oauth/token with grant_type=refresh_token

The browser redirect to https://tradeapi.samco.in/app/oauth/authorize?... is
out of band — this file handles the backend-only steps.

Reference: https://docs-tradeapi.samco.in/oauth/authorize-flow

Install once: pip install requests
Run:          python oauth_exchange.py
"""

import requests

BASE_URL = "https://tradeapi.samco.in"


def exchange_code(code: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,  # single-use, valid 10 minutes
        },
    ).json()

    if r.get("status") != "Success" or "data" not in r:
        raise RuntimeError(f"Token exchange failed: {r.get('message', 'unknown')}")
    return r["data"]


def refresh_access_token(refresh_token: str) -> dict:
    # The old refresh_token is invalidated when this call succeeds —
    # persist the new pair atomically.
    r = requests.post(
        f"{BASE_URL}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    ).json()

    if r.get("status") != "Success" or "data" not in r:
        raise RuntimeError(f"Refresh failed: {r.get('message', 'unknown')}")
    return r["data"]


def get_holdings(access_token: str) -> dict:
    headers = {
        "Accept": "application/json",
        "x-session-token": access_token,
    }
    return requests.get(f"{BASE_URL}/holding/getHolding", headers=headers).json()


if __name__ == "__main__":
    # In a real app, `code` is the value you received on your callback URL:
    #   https://your-app.example.com/callback?code=<AUTH_CODE>&state=<ECHOED_STATE>
    AUTH_CODE = "<AUTH_CODE_FROM_CALLBACK>"

    # Step 1: Exchange code for access_token + refresh_token
    session = exchange_code(AUTH_CODE)
    print("accountID:    ", session["accountID"])
    print("access_token: ", session["access_token"][:24], "...")
    print("expires_in:   ", session["expires_in"], "seconds")

    # Step 2: Use access_token as `x-session-token` on Trade API calls
    holdings = get_holdings(session["access_token"])
    print("Holdings:", holdings)

    # Step 3: Refresh near expiry (or within the 7-day refresh window)
    session = refresh_access_token(session["refresh_token"])
    print("Refreshed access_token:", session["access_token"][:24], "...")
