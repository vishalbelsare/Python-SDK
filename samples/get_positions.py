"""
GET /position/getPositions?positionType=<DAY|NET>

Current intraday (DAY) or carry-forward (NET) positions for the
authenticated account.

Reference: https://docs-tradeapi.samco.in/positions/get-positions

Run: python get_positions.py
"""

import json
import os
import requests

from config import BASE_URL, load_env, require_session_token


def get_positions(session_token: str, position_type: str = "NET") -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    params = {"positionType": position_type}

    r = requests.get(
        f"{BASE_URL}/position/getPositions", headers=headers, params=params
    )
    payload = r.json()
    if payload.get("status") != "Success":
        raise RuntimeError(f"Get positions failed: {payload.get('statusMessage')}")
    return payload


def main() -> None:
    load_env()
    token = require_session_token()

    position_type = os.environ.get("SAMCO_POSITION_TYPE", "NET")
    result = get_positions(token, position_type)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
