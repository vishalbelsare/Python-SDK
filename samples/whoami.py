"""
GET /ip/whoami

Read-only diagnostic. Returns the source IP our server sees plus your
currently-registered PRIMARY / SECONDARY IPs and whether the source
matches. Does NOT consume your SEBI weekly IP-update slot.

Reference: https://docs-tradeapi.samco.in/static-ip/whoami

Run: python whoami.py
"""

import json
import sys
import requests

from config import BASE_URL, load_env, require_session_token


def whoami(session_token: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    return requests.get(f"{BASE_URL}/ip/whoami", headers=headers).json()


def main() -> None:
    load_env()
    token = require_session_token()

    result = whoami(token)
    print(json.dumps(result, indent=2))

    if not result.get("matches"):
        print(
            f"WARNING: This host's source IP {result.get('srcIp')} is not "
            "registered. Order endpoints will reject this host with HTTP 403. "
            "Update your registered IP via the Web Dashboard → Static IPs.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
