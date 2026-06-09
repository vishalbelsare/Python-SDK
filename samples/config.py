"""
Shared helpers for the v3.2 samples — env loading, credential validation,
and the section/skipped logging used by quick_start.py. Mirrors the
helpers in Java's QuickStartSample and Node's quickStart.ts.
"""

import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None  # noqa: N816

BASE_URL = "https://tradeapi.samco.in"
STREAM_URL = "wss://stream.samco.in"

_TRUE = {"1", "true", "yes", "on"}


def load_env() -> None:
    """Load samples/.env if python-dotenv is installed. Idempotent."""
    if load_dotenv is not None:
        load_dotenv()


def is_placeholder(s: str) -> bool:
    s = (s or "").strip()
    return s.startswith("<") and s.endswith(">")


def flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in _TRUE


def require_real_credentials() -> tuple[str, str]:
    api_key = (os.environ.get("SAMCO_API_KEY") or "").strip()
    api_secret = (os.environ.get("SAMCO_API_SECRET") or "").strip()
    if not api_key or not api_secret or is_placeholder(api_key) or is_placeholder(api_secret):
        raise RuntimeError(
            "SAMCO_API_KEY / SAMCO_API_SECRET are missing or still placeholders. "
            "Edit samples/.env with your AES-encrypted credentials before running."
        )
    return api_key, api_secret


def require_session_token() -> str:
    token = (os.environ.get("SAMCO_SESSION_TOKEN") or "").strip()
    if not token or is_placeholder(token):
        raise RuntimeError(
            "SAMCO_SESSION_TOKEN is missing or still a placeholder. "
            "Run `python session_token.py` and paste the JWT into samples/.env."
        )
    return token


def section(title: str) -> None:
    print(f"\n==== {title} ====")


def skipped(title: str, reason: str) -> None:
    print(f"\n---- {title} (skipped: {reason}) ----")
