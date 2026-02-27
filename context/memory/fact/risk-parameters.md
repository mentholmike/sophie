# Risk Parameters

> ⚠️ **MANDATORY: Read before trading. If you skip this, you lose your edge.**

## Trading Parameters

| Parameter | Value |
|-----------|-------|
| Min edge | **3%** |
| Max position | **$25** |
| Min bet | **$1** |
| Max loss alerts | 3 losses in 6h → pause |

---

## Conviction Scoring (Enhanced - Feb 24, 2026)

**Philosophy:**
- Reputation × Confidence approach (not penalty-based)
- 1hr expiry for hourly crypto is NORMAL, not a penalty
- Weather: Earlier entry = more edge (forecasts converge)

```
CONVICTION = (Base + Edge + Data + Structure) × Confidence

Base = 50
Edge = Market mispricing (0-40)
Data = Research quality (0-25)
Structure = Resolution clarity (0-15)

Confidence = Time × Liquidity × Spread
- Time: >30min=1.0, 15-30=0.9, <15=0.7
- Liquidity: >$20k=1.0, $5-20k=0.9, <$5k=0.7
- Spread: <2%=1.0, 2-5%=0.9, >5%=0.8
```

**Tier Sizing:**
| Score | Tier | Size |
|-------|------|------|
| 30-49 | Low | $1-3 |
| 50-69 | Medium | $3-5 |
| 70-84 | High | $5-10 |
| 85+ | Maximum | $10-15 |

**Auto-Trade Rule:**
- Conviction ≥70% + Edge ≥5% → AUTO BUY

---

## Liquidity Requirements

- **MIN LIQUIDITY:** $2,000+ (bid+ask combined)
- **MAX BID-ASK SPREAD:** <10%
- **MIN VOLUME (24h):** $5,000+

---

## LIQUIDITY BAN (CRITICAL)

**This is a hard rule. NO exceptions. NO illiquid markets.**

We lost ~$25 on Ethena slippage. Never again.

### Scanner Must Check Before EVERY Trade:

1. **Get order book via Vincent API:**
   ```
   GET /api/skills/polymarket/orderbook/<TOKEN_ID>
   ```

2. **Calculate total bid depth at top 3 levels** (sum of bid sizes × prices)

3. **Calculate total ask depth at top 3 levels** (sum of ask sizes × prices)

4. **Calculate spread:**
   ```
   Spread = (ask - bid) / midpoint × 100
   ```

### Hard Thresholds (ALL must pass):

| Metric | Threshold |
|--------|-----------|
| Bid depth (top 3) | ≥ $100 |
| Ask depth (top 3) | ≥ $100 |
| Spread | ≤ 10% |

**If ANY fail → SKIP, do not trade. This is non-negotiable.**

### Why This Matters

Illiquid markets = massive slippage when entering AND exiting. A $10 bet turns into $15 loss because you can't get out at fair price. The liquidity check prevents both:
- Entering bad markets
- Getting trapped with no exit

**This applies to BOTH scanner AND scalper exits.**

---

## Exit Logic

### Two-Step Exit Framework
1. **Bank 70%** when scalp trigger hit
2. **Trail 30%** with trailing-stop

### Scalp Targets
- 5m/15m: 15-25%+
- 1h: 8%+
- Longer: capital-based ladder

### Time Stops
- 5m ≈ 1m before expiry
- 15m ≈ 3m before expiry
- 1h ≈ 10m before expiry

### Hard Stops
- **Auto-close at -30%** PnL
- **Conviction floor:** close if conviction <= 60 OR drift >15pts

---

## Loss Alert Threshold

- **3 losses in 6h** → pause auto-trades, notify user
- Resume: manual `/resume_trades` or 6h elapsed
- Loss = trade with ≤-5% PnL at exit

### Auto-Rebalance
- After 3 consecutive losses → reduce bet size to $3
- Require manual `/resume_trades` to restore

---

## Weather Market Rules

1. **Verify end time makes sense** for the metric
2. For "daily high" → end time should be 24h later
3. Scan day-before pre-dawn (TAF/models), bet 4-11AM day-of (METAR)
4. Market status check: OPEN vs CLOSED vs RESOLVED

---

## Crypto Market Rules

1. **"Bitcoin Up or Down"** = 1-hour candle DIRECTION, not level
2. **Static level markets:** BTC > $X at time T
3. **Direction markets:** Up/Down in that hour
4. Resolution source: Binance BTC/USDT 1-hour candle

### Hourly Crypto Edge Detection

**Scan Frequency:** Every 5 minutes during active trading hours

**Required for EVERY crypto hourly scan:**

1. **Coinbase spot API** - Get current price
   ```
   curl https://api.coinbase.com/v2/prices/BTC-USD/spot
   ```

2. **Dynamic slug generation** - ALL FOUR coins:
   ```bash
   MONTH=$(date +"%B" | tr '[:upper:]' '[:lower:]')
   DAY=$(date +"%-d")
   HOUR_12=$(date +"%-I")
   AMPM=$(date +"%p" | tr '[:upper:]' '[:lower:]')
   
   # All four coins (NOT just BTC!)
   bitcoin-up-or-down-${MONTH}-${DAY}-${HOUR_12}${AMPM}-et
   ethereum-up-or-down-${MONTH}-${DAY}-${HOUR_12}${AMPM}-et
   solana-up-or-down-${MONTH}-${DAY}-${HOUR_12}${AMPM}-et
   xrp-up-or-down-${MONTH}-${DAY}-${HOUR_12}${AMPM}-et
   ```

3. **Vincent market search** - Query all four slugs:
   ```
   GET /api/skills/polymarket/markets?query={slug}&limit=1
   ```

4. **Edge assessment** - Compare Polymarket price vs spot:
   - If market at 45-55% → fair value (no edge)
   - If market at 30-44% or 56-70% → potential edge
   - Apply reputation penalties before committing

**Never scan just BTC - always do all four coins.**

### Market Sentiment (Fear & Greed)

**Required for EVERY crypto scan:**
```
curl -s https://api.alternative.me/fng/ | jq '.data[0] | {value: .value, classification: .value_classification}'
```

**Interpretation:**
- 0-25: Extreme Fear — potential buying opportunity
- 25-50: Fear — slightly bearish
- 50-75: Greed — slightly bullish
- 75-100: Extreme Greed — potential selling opportunity

**Use in edge assessment:** Extreme Fear + market at 45-55% = potential edge (contrarian). Extreme Greed + heavy one-sided price = potential overvaluation.

### Deep Research (DuckDuckGo)

**When to use:**
- Major market moves (>5% in an hour)
- Unusual Polymarket pricing (e.g., ETH flipping 76%→25% in 1hr)
- Before entering positions >$10
- News-driven events (earnings, ETF decisions, regulatory)

**How to use:**
```bash
python3 -c "
from duckduckgo_search import DDGS
with DDGS() as ddgs:
    results = list(ddgs.text('bitcoin news february 23 2026', max_results=5))
    for r in results:
        print(f'- {r[\"title\"]}: {r[\"href\"]}')
"
```

**Apply findings to edge assessment** — if news supports directional thesis, increase conviction. If contradicts, decrease.

### On-Chain & Funding Data (Loris Tools)

**API Endpoint:**
```
curl -s https://api.loris.cccagg.com/?c=binance&m=funding | jq '.funding_intervals.binance.BTC'
```

**What it shows:**
- Funding intervals (when funding settles: 4h, 8h)
- Which exchanges support which symbols
- Cross-exchange comparison capability

**Use for:**
- Detect extreme funding (longs/shorts heavily stacked)
- Compare funding across exchanges for arbitrage
- Identify which coins have active perpetual markets

**Note:** Actual funding rates (0.01%, -0.05%, etc.) may require different endpoint.

### Coinalyze API (Real-Time Funding & OI)

**API Key:** Stored in ~/.env (source it before use)

**Format:** Use `.PERP.A` suffix (e.g., `BTCUSDT_PERP.A`)

**Endpoints:**
```
# Funding rates (real-time, % per interval)
curl -s "https://api.coinalyze.net/v1/funding-rates?symbols=BTCUSDT_PERP.A" \
  -H "api_key: $COINALYZE_API_KEY"

# Open interest ($ value)
curl -s "https://api.coinalyze.net/v1/open-interest?symbols=BTCUSDT_PERP.A" \
  -H "api_key: $COINALYZE_API_KEY"
```

**Edge signals:**
- Negative funding = shorts paying longs (longs cost money, shorts earn)
- Extreme funding (>0.1% per 8h) = potential reversal (overleveraged)
- Spiking OI = increasing leverage = higher liquidation risk
