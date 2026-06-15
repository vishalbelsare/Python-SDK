# SAMCO Trade API v3.2 — Python samples

Runnable Python clients for the v3.2 endpoints documented in
[`ta-api-docs`](https://docs-tradeapi.samco.in). REST samples are plain
`requests` (no SDK dependency) so they read 1:1 against the docs.
`streaming_quote.py` and `streaming_market_data.py` drive the websocket
through the published `stocknotebridge` (`snapi_py_client`) SDK
(>= 3.2.2 — see TRD-1467 streamer fix); `sample_client.py` is the
full REST + streaming flow expressed through the same SDK.

## Install

```bash
cd samples
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or: pip install .     (uses pyproject.toml)
# then create samples/.env with your AES-encrypted credentials
```

Requires **Python 3.8+**.

Packaging is declared in `pyproject.toml` (PEP 621), the modern Python
equivalent of `package.json` / `pom.xml`. `requirements.txt` is kept as
a simple flat dependency list for `pip install -r` workflows.

Installing with `pip install .` also exposes console-script shortcuts
(`samco-session-token`, `samco-whoami`, `samco-get-quote`,
`samco-place-order`, `samco-order-book`, `samco-order-status`,
`samco-get-positions`, `samco-get-holdings`, `samco-stream-quote`,
`samco-stream-market-data`, `samco-sample-client`, `samco-quick-start`)
so each sample can be run without the `python <file>.py` prefix.

## Environment variables

Create `samples/.env` (auto-loaded by every sample via `python-dotenv`)
or export the variables in your shell:

| Var                     | Used by                                                                    |
|-------------------------|----------------------------------------------------------------------------|
| `SAMCO_API_KEY`         | `session_token.py`, `sample_client.py`, `quick_start.py`                   |
| `SAMCO_API_SECRET`      | `session_token.py`, `sample_client.py`, `quick_start.py`                   |
| `SAMCO_SESSION_TOKEN`   | `whoami.py`, `get_quote.py`, `place_order.py`, `streaming_quote.py`, `streaming_market_data.py` |
| `SAMCO_QUOTE_SYMBOL`    | `get_quote.py` — optional override (default `SBIN`)                        |
| `SAMCO_QUOTE_EXCHANGE`  | `get_quote.py` — optional override (default `NSE`)                         |
| `SAMCO_POSITION_TYPE`   | `get_positions.py` — optional override, `DAY` or `NET` (default `NET`)     |
| `SAMCO_ORDER_NUMBER`    | `order_status.py` — **required** order number to query                     |
| `SAMCO_RUN_PLACE_ORDER` | `quick_start.py`, `sample_client.py` — `true` includes the destructive place-order step |
| `SAMCO_RUN_STREAMING`   | `quick_start.py` — `true` runs each streaming sample ~60 s then exits      |

Both `SAMCO_API_KEY` and `SAMCO_API_SECRET` must be the **AES-encrypted**
values delivered when the OAuth app was created.

Example `samples/.env`:

```
SAMCO_API_KEY=<AES_ENCRYPTED_API_KEY>
SAMCO_API_SECRET=<AES_ENCRYPTED_API_SECRET>
SAMCO_SESSION_TOKEN=<SESSION_TOKEN>
SAMCO_RUN_PLACE_ORDER=false
SAMCO_RUN_STREAMING=false
```

## Scripts

| Command                                  | Endpoint                                   | Source doc                                  |
|------------------------------------------|--------------------------------------------|---------------------------------------------|
| `python session_token.py`                | `POST /session/token`                      | `session/generate-token.md`                 |
| `python whoami.py`                       | `GET /ip/whoami`                           | `static-ip/whoami.md`                       |
| `python get_quote.py`                    | `GET /quote/getQuote`                      | `quote/get-quote.md`                        |
| `python place_order.py`                  | `POST /order/placeOrder` (LIMIT)           | `order/place-order.md`                      |
| `python order_book.py`                   | `GET /order/orderBook`                     | `order/order-book.md`                       |
| `python order_status.py`                 | `GET /order/getOrderStatus`                | `order/get-order-status.md`                 |
| `python get_positions.py`                | `GET /position/getPositions`               | `positions/get-positions.md`                |
| `python get_holdings.py`                 | `GET /holding/getHoldings`                 | `holdings/get-holdings.md`                  |
| `python streaming_quote.py`              | `wss://stream.samco.in` (`quote`) via SDK  | `streaming/streaming-quote-data.md`         |
| `python streaming_market_data.py`        | `wss://stream.samco.in` (`quote2`, depth) via SDK | `streaming/streaming-market-data.md`  |
| `python sample_client.py`                | End-to-end flow via `stocknotebridge` SDK  | (SDK walkthrough)                           |
| `python quick_start.py`                  | Runs every sample above in sequence        | (mirrors Java `QuickStartSample`)           |

## Quick start

```bash
# Edit samples/.env: set SAMCO_API_KEY / SAMCO_API_SECRET, then:
python quick_start.py        # session-token → whoami → quote → (opt) place-order → (opt) streaming
```

`quick_start.py` reads `SAMCO_RUN_PLACE_ORDER` and `SAMCO_RUN_STREAMING`
from `.env` to opt in/out of the destructive and long-running steps.

## Running samples individually

```bash
# 1. Get a session token (prints the JWT).
python session_token.py

# 2. Paste the JWT into SAMCO_SESSION_TOKEN in .env, then:
python whoami.py
python get_quote.py                # defaults to SBIN @ NSE
python get_holdings.py             # CNC holdings snapshot
python get_positions.py            # NET positions (set SAMCO_POSITION_TYPE=DAY for intraday)
python order_book.py               # today's orders
SAMCO_ORDER_NUMBER=240207000133590 python order_status.py
python place_order.py              # LIMIT order — review DEFAULT_ORDER in place_order.py first
python streaming_quote.py          # Ctrl-C to unsubscribe + close
python streaming_market_data.py    # Ctrl-C to unsubscribe + close
```

> ⚠ **`place_order.py` and `quick_start.py` with `SAMCO_RUN_PLACE_ORDER=true`
> hit live trading endpoints.** SAMCO does not provide a sandbox — a
> successful call places a real order on your account and can affect your
> balances and positions. Review every field — symbol, quantity, price,
> side — before running.

## Common errors

**`EOAUTH001` / `EOAUTH008` — "Invalid API key" / "Invalid API secret"**
You probably pasted the plaintext value instead of the AES-encrypted form,
or the value is from a different environment. Go to **Web Dashboard →
API Keys → Reveal Secret** and copy the encrypted string as-is into
`SAMCO_API_KEY` / `SAMCO_API_SECRET`.

**`HTTP 403 — The IP is not the registered static IP`**
Your host's source IP is not in your allowlist. Run `python whoami.py`
from the same host to see the exact IP our server sees, then update your
registered IPs at [Web Dashboard → Static IPs](https://tradeapi.samco.in/app/static-ips).
Note that `/ip/whoami` itself does not require an IP match.

**`401 — Unauthorized. Session token is mandatory.`**
You forgot to set `SAMCO_SESSION_TOKEN` in `.env`, or the token has
expired (it is valid only until 08:00 IST the next day). Re-run
`python session_token.py` to mint a fresh one.

**`"Unable to start your trading session"`**
The `apiKey` / `apiSecret` were accepted, but SAMCO's trading backend
can't establish a session for the underlying account. The account holder
must sign in once on the SAMCO mobile app (or
[Samco Web](https://www.samco.in)) and then retry. If the account is
blocked / dormant, contact [apisupport@samco.in](mailto:apisupport@samco.in).

## Reference

- Full v3.2 API docs: <https://docs-tradeapi.samco.in>
- Release notes: <https://docs-tradeapi.samco.in/release-notes/v3.2.0>
- Java samples (parity reference): `../../Java-SDK/samples/README.md`
- Node samples (parity reference): `../../NodeJS-SDK/samples/README.md`
