# Samples — How to run

Runnable Python clients for the **v3.2** SAMCO Trade API endpoints that the published `snapi_py_client` (v3.2.0) does not yet wrap as helper methods. They speak HTTP/WebSocket directly with `requests` / `websocket-client`.

| # | File | Endpoint |
|---|---|---|
| 1 | [`session_token.py`](./session_token.py) | `POST /session/token` — direct JWT auth |
| 2 | [`whoami.py`](./whoami.py) | `GET /ip/whoami` — IP diagnostic |
| 3 | [`oauth_exchange.py`](./oauth_exchange.py) | `POST /oauth/token` — code exchange + refresh + holdings |
| 4 | [`get_quote.py`](./get_quote.py) | `GET /quote/getQuote` |
| 5 | [`place_order.py`](./place_order.py) | `POST /order/placeOrder` (LIMIT) — **live trading, no sandbox** |
| 6 | [`streaming_quote.py`](./streaming_quote.py) | `wss://stream.samco.in` `streaming_type: "quote"` |
| 7 | [`streaming_market_data.py`](./streaming_market_data.py) | `wss://stream.samco.in` `streaming_type: "quote2"` (5-level depth) |

---

## Prerequisites

- **Python 3.8+** and `pip`. No Maven (`pom.xml`), Gradle, or `npm` — these are pure Python scripts.
- An **OAuth app** created at the [SAMCO Trade API Web Dashboard → API Keys](https://tradeapi.samco.in/app/api-keys). You need the AES-encrypted **API Key** (mailed to you) and **API Secret** (shown once on creation).
- A **Static IP** registered for the app at [Web Dashboard → Static IPs](https://tradeapi.samco.in/app/static-ips). Order endpoints reject requests from non-whitelisted IPs.

---

## One-time setup

```bash
cd samples/
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` (now next to this README) pins `requests>=2.32.0`, `websocket-client>=1.7.0`, and friends. That covers every sample below.

---

## Get a session token first

Every sample **except** `session_token.py` (which produces the token) and `oauth_exchange.py` (which produces its own `access_token`) needs you to replace the `<SESSION_TOKEN>` placeholder inside the file with a real JWT.

Two ways to get one:

### A. Direct (headless / server-to-server) — recommended for backend bots

1. Open `session_token.py` and replace `<AES_ENCRYPTED_API_KEY>` / `<AES_ENCRYPTED_API_SECRET>` with the values from the Web Dashboard.
2. Run it:
   ```bash
   python session_token.py
   ```
3. Copy the printed `sessionToken: eyJhbGc...` value.
4. Paste it into the `<SESSION_TOKEN>` placeholder in whichever other sample you want to run.

The token is valid until **08:00 IST the next day**. After that, re-run `session_token.py` to obtain a fresh one.

### B. OAuth 2.1 Authorization-Code Flow — for third-party apps signing in end-users

1. Redirect the user's browser to `https://tradeapi.samco.in/app/oauth/authorize?api_key=...&redirect_url=...&state=...`. This step is out of scope for the script.
2. On your callback URL you receive `?code=<AUTH_CODE>&state=...`. Paste `<AUTH_CODE>` into `oauth_exchange.py`'s `AUTH_CODE` constant.
3. Run it:
   ```bash
   python oauth_exchange.py
   ```
4. Use the printed `access_token` as `<SESSION_TOKEN>` in the other samples.

---

## Per-sample run guide

In every case: edit the placeholder constants at the top of the file, then `python <file>.py`.

| File | Placeholders to edit | Command | What you should see |
|---|---|---|---|
| `session_token.py` | `<AES_ENCRYPTED_API_KEY>`, `<AES_ENCRYPTED_API_SECRET>` | `python session_token.py` | `accountID`, `srcIp`, truncated JWT, then `Holdings: {...}` |
| `whoami.py` | `<SESSION_TOKEN>` | `python whoami.py` | `srcIp`, `primaryIp`, `secondaryIp`, `matches: true/false`. Exits 1 if `matches: false`. |
| `oauth_exchange.py` | `<AUTH_CODE_FROM_CALLBACK>` | `python oauth_exchange.py` | `accountID`, truncated `access_token`, holdings, then a refreshed token |
| `get_quote.py` | `<SESSION_TOKEN>` (and optionally the `symbol_name` / `exchange` args) | `python get_quote.py` | symbol, LTP, previous close, change, OHLC, top bid / ask |
| `place_order.py` | `<SESSION_TOKEN>` (and the `limit_order` dict — symbol, qty, price) | `python place_order.py` | `orderNumber`, `exchangeOrderStatus: PENDING`, full order echo |
| `streaming_quote.py` | `<SESSION_TOKEN>` (and the symbols list) | `python streaming_quote.py` | `Connected`, then a stream of `Quote :: {...}` frames. Ctrl-C unsubscribes cleanly. |
| `streaming_market_data.py` | `<SESSION_TOKEN>` (and the symbols list) | `python streaming_market_data.py` | `Connected`, then `Market data :: {...}` frames with 5-level depth. Ctrl-C unsubscribes cleanly. |

> ⚠ **`place_order.py` is a live trading endpoint.** SAMCO does not provide a sandbox. A successful call places a real order on your account and can affect your balances and positions. Review every field — symbol, quantity, price, side — before running.

---

## Common errors

**`EOAUTH001` / `EOAUTH008` — "Invalid API key" / "Invalid API secret"**
You probably pasted the plaintext value instead of the AES-encrypted form, or the value is from a different environment. Go to **Web Dashboard → API Keys → Reveal Secret** and copy the encrypted string as-is.

**`HTTP 403 — The IP is not the registered static IP`**
Your host's source IP is not in your allowlist. Run `python whoami.py` from the same host to see the exact IP our server sees, then update your registered IPs at [Web Dashboard → Static IPs](https://tradeapi.samco.in/app/static-ips). Note that `/ip/whoami` itself does not require an IP match.

**`401 — Unauthorized. Session token is mandatory.`**
You forgot to replace `<SESSION_TOKEN>` in the file, or the token has expired (it is valid only until 08:00 IST the next day). Re-run `session_token.py` to mint a fresh one.

**`"Unable to start your trading session"`**
The `apiKey` / `apiSecret` were accepted, but SAMCO's trading backend can't establish a session for the underlying account. The account holder must sign in once on the SAMCO mobile app (or [Samco Web](https://www.samco.in)) and then retry. If the account is blocked / dormant, contact [apisupport@samco.in](mailto:apisupport@samco.in).

---

## Reference

- Full v3.2 API docs: <https://docs-tradeapi.samco.in>
- Release notes: <https://docs-tradeapi.samco.in/release-notes/v3.2.0>
- The corresponding inline snippets in the [project README](../README.md#v32-apis--sample-client-code) are kept in sync with these files.
