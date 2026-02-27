# API Configuration

> ⚠️ **MANDATORY: Read before trading. Contains Vincent endpoints.**
> 
> **Note:** All API keys are stored in `/.openclaw/secrets/.env`. Source it before use:
> ```bash
> source /.openclaw/secrets/.env
> ```
> 
> ⚠️ **IMPORTANT:** The `.gitignore` file is ABSOLUTE — never commit secrets, credentials, or `.env`. This is non-negotiable.

## Vincent Wallet (PRIMARY TRADING)

**Created:** 2026-02-16
**Wallet Address:** `0x4e56fe13d01fd6217243020e5dcc040b021d2493`
**API Key:** Get from `~/.openclaw/credentials/agentwallet/cmloigqm30003i8r0hjqdc5wr.json` → field `apiKey`
**Skill Reference:** `skills/vincentpolymarket/SKILL.md`

### Vincent API Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| Balance | GET | `/api/skills/polymarket/balance` |
| Holdings | GET | `/api/skills/polymarket/holdings` |
| Open Orders | GET | `/api/skills/polymarket/positions` |
| Search Markets | GET | `/api/skills/polymarket/markets?query=<keyword>` |
| Market Details | GET | `/api/skills/polymarket/market/<CONDITION_ID>` |
| Order Book | GET | `/api/skills/polymarket/orderbook/<TOKEN_ID>` |
| Place Bet | POST | `/api/skills/polymarket/bet` |
| Cancel Order | DELETE | `/api/skills/polymarket/orders/<ORDER_ID>` |
| Cancel All | DELETE | `/api/skills/polymarket/orders` |

### Auth Header
```
Authorization: Bearer $VINCENT_API_KEY
```

### Place Bet Payload
```json
{
  "tokenId": "<OUTCOME_TOKEN_ID>",
  "side": "BUY",
  "amount": 5,
  "price": 0.55
}
```
- `amount` = USD to spend (BUY) or shares to sell (SELL)
- `price` = limit price (optional for market order)
- Minimum bet: $1

### Important Notes
- **tokenIds array**: Index 0 = Yes, Index 1 = No
- **Gasless**: All transactions via Polymarket relayer
- **Settlement**: Wait a few seconds after BUY before SELL
- **Fund with USDC.e only** (bridged USDC on Polygon): `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`

### Crypto Market Slug Formats (CRITICAL)

**Format:** `(asset)-up-or-down-(month)-(date)-(time)-et`

| Asset | Slug Examples |
|-------|---------------|
| **BTC** | `bitcoin-up-or-down-february-24-4pm-et` |
| **ETH** | `ethereum-up-or-down-february-24-4pm-et` |
| **SOL** | `solana-up-or-down-february-24-4pm-et` |
| **XRP** | `xrp-up-or-down-february-24-4pm-et` |

**Note:** Use full month name (lowercase), 12-hour format without space (4pm not 4-pm or 16:00).

### Search Patterns for Vincent API (Use These)
```bash
# Source env first
source /.openclaw/secrets/.env

# BTC hourly
curl -H "Authorization: Bearer $VINCENT_API_KEY" \
  "https://heyvincent.ai/api/skills/polymarket/markets?query=bitcoin-up-or-down-february-24&limit=20"

# ETH hourly
curl -H "Authorization: Bearer $VINCENT_API_KEY" \
  "https://heyvincent.ai/api/skills/polymarket/markets?query=ethereum-up-or-down-february-24&limit=20"

# SOL hourly
curl -H "Authorization: Bearer $VINCENT_API_KEY" \
  "https://heyvincent.ai/api/skills/polymarket/markets?query=solana-up-or-down-february-24&limit=20"

# XRP hourly
curl -H "Authorization: Bearer $VINCENT_API_KEY" \
  "https://heyvincent.ai/api/skills/polymarket/markets?query=xrp-up-or-down-february-24&limit=20"

# Weather markets
curl -H "Authorization: Bearer $VINCENT_API_KEY" \
  "https://heyvincent.ai/api/skills/polymarket/markets?query=temperature&limit=20"
```

### Coinalyze API (On-Chain Data)
```bash
source /.openclaw/secrets/.env
curl -s "https://api.coinalyze.net/v1/funding-rate?symbols=BTCUSDT_PERP.A" \
  -H "api_key: $COINALYZE_API_KEY"
```

## Subagent Trading System

### Market Scanner Agent
- **Runs:** Every 5 minutes (2 hour sessions)
- **Task:** Scan BTC/ETH/SOL/XRP hourly markets, execute trades
- **Triggers:** Conviction ≥70% + Edge ≥5%
- **Size:** $5 (70-84%), $10 (85%+)
- **CRITICAL:** Use MARKET ORDERS only (omit "price" field)

### Scalper Agent
- **Runs:** Every 2 minutes (2 hour sessions)
- **Task:** Monitor positions, execute exits
- **Current Time:** Use `date` command to get current time for context
- **Filter ACTIVE positions (CRITICAL - must filter before checking):**
  - `endDate` >= today's date (skip expired markets)
  - `currentPrice` > 0 (skip resolved positions)
  - `pnlPercent` > -100 (skip already-zeroed positions)
- **Exit rules (in order):**
  1. **Skip if already exited:** Track position IDs that triggered exit this session, don't re-process
  2. **+7.3% to +15% PnL:** Sell 70%, keep 30% → SEND NOTIFICATION: `message(action=send, message="✅ PROFIT: [Market] - +X%", channel="telegram")`
  3. **Above +15% PnL:** Sell ALL (full exit) → SEND NOTIFICATION: `message(action=send, message="🎯 MAX PROFIT: [Market] - +X%", channel="telegram")`
  4. **-35% PnL:** Sell ALL (hard stop) → SEND NOTIFICATION: `message(action=send, message="🛑 STOP LOSS: [Market] - X%", channel="telegram")`
- **CRITICAL:** Use MARKET ORDERS only (omit "price" field)

### Active Position Filter
Only check positions where:
- `endDate` >= today's date
- `pnlPercent` > -100 (not already at $0)
- `currentPrice` > 0 (not resolved)

### Spawn Commands (Feb 24, 2026 - Updated with logging)

**Scanner:**
```
Run market scanner for 2 hours. At each cycle (every 5 min):
1. Run: source /.openclaw/secrets/.env && bash comprehensive_scan.sh
2. Parse output for ">>> AUTO INVEST" signals
3. If signal: check for existing position, then place bet using Vincent API (market order)
4. If trade placed: SEND NOTIFICATION via message(action=send, message="🔔 NEW TRADE: [Market] - [Amount] @ [Price]")
5. APPEND result to memory/scanner-YYYY-MM-DD.md
6. Sleep 300 and repeat.
```

**Scalper:**
```
Current time: $(date)

Run scalp exit monitor for 2 hours. At each cycle (every 2 min):
1. Get current time: date
2. Get holdings via Vincent API
3. FILTER ACTIVE positions (CRITICAL - skip if ANY fail):
   - endDate >= today's date (skip expired)
   - currentPrice > 0 (skip resolved)
   - pnlPercent > -100 (skip zeroed)
4. Track exited position IDs - skip if already processed this session
5. Apply exit rules:
   - +7.3% to +15%: Sell 70%, keep 30% → SEND NOTIFICATION: `message(action=send, message="✅ PROFIT: [Market] - +X%", channel="telegram")`
   - Above +15%: Sell ALL → SEND NOTIFICATION: `message(action=send, message="🎯 MAX PROFIT: [Market] - +X%", channel="telegram")`
   - -35%: Sell all (stop loss) → SEND NOTIFICATION: `message(action=send, message="🛑 STOP LOSS: [Market] - X%", channel="telegram")`
6. Log exits to memory/scalper-YYYY-MM-DD.md
7. Sleep 120 and repeat.
```

### Check Subagent Status
```bash
subagents(action=list)
```
