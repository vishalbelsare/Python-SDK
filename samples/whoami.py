"""
GET /ip/whoami

Read-only diagnostic. Returns the source IP our server sees plus your
currently-registered PRIMARY / SECONDARY IPs and whether the source
matches. Does NOT consume your SEBI weekly IP-update slot.

Reference: https://docs-tradeapi.samco.in/static-ip/whoami

Install once: pip install requests
Run:          python whoami.py
"""

import sys
import requests

BASE_URL = "https://tradeapi.samco.in"


def whoami(session_token: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-session-token": session_token,
    }
    return requests.get(f"{BASE_URL}/ip/whoami", headers=headers).json()


if __name__ == "__main__":
    SESSION_TOKEN = "<SESSION_TOKEN>"

    result = whoami(SESSION_TOKEN)

    print("srcIp:       ", result.get("srcIp"))
    print("primaryIp:   ", result.get("primaryIp"))
    print("secondaryIp: ", result.get("secondaryIp"))
    print("matches:     ", result.get("matches"))
    print("matchedAs:   ", result.get("matchedAs"))

    if not result.get("matches"):
        print(
            f"WARNING: This host's egress IP {result.get('srcIp')} is not "
            f"registered. Order endpoints will reject this host with HTTP 403. "
            f"Update your registered IP via the Web Dashboard → Static IPs.",
            file=sys.stderr,
        )
        sys.exit(1)
