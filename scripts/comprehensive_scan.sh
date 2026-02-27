#!/bin/bash
# Comprehensive Market Scan Script
# Usage: source /.openclaw/secrets/.env && bash comprehensive_scan.sh
# Outputs: Portfolio, Holdings, Edge Analysis with Conviction Scores

NOW=$(date +"%H:%M %Z")
DAY=$(date +%-d)
MONTH=$(date +"%B" | tr '[:upper:]' '[:lower:]')
HR=$(date +"%-I")
AP=$(date +"%p" | tr '[:upper:]' '[:lower:]')

echo "================================================================"
echo "          COMPREHENSIVE MARKET SCAN - $NOW"
echo "================================================================"
echo ""

# Portfolio
BALANCE=$(curl -s -H "Authorization: Bearer $VINCENT_API_KEY" "https://heyvincent.ai/api/skills/polymarket/balance" | jq -r '.data.collateral.balance')
echo "=== PORTFOLIO ==="
echo "Balance: \$$BALANCE USDC.e"
echo ""

# Holdings
echo "=== HOLDINGS (Today) ==="
curl -s -H "Authorization: Bearer $VINCENT_API_KEY" "https://heyvincent.ai/api/skills/polymarket/holdings" | \
  jq -r '.data.holdings[] | select(.endDate == "2026-02-24") | "\(.marketTitle[0:35]): \(.pnlPercent)%"' 2>/dev/null || echo "No open positions"
echo ""

# Market Data
FG=$(curl -s "https://api.alternative.me/fng/?limit=1" | jq -r '.data[0].value')
FG_CLASS=$(curl -s "https://api.alternative.me/fng/?limit=1" | jq -r '.data[0].value_classification')
BTC=$(curl -s "https://api.exchange.coinbase.com/products/BTC-USD/ticker" | jq -r '.price')

echo "=== MARKET METRICS ==="
echo "BTC: \$$BTC | Fear & Greed: $FG ($FG_CLASS)"
echo ""

# Funding rates
echo "=== FUNDING ==="
curl -s "https://api.coinalyze.net/v1/funding-rate?symbols=BTCUSDT_PERP.A,ETHUSDT_PERP.A,SOLUSDT_PERP.A,XRPUSDT_PERP.A" \
  -H "api_key: $COINALYZE_API_KEY" 2>/dev/null | \
  jq -r '.[] | "  \(.symbol): \(.value)%"' 2>/dev/null
echo ""

# Edge Analysis
echo "=== EDGE ANALYSIS ($HR$AP) ==="
echo ""

python3 << 'PYEOF'
import os, json, requests, datetime

api_key = os.environ.get('VINCENT_API_KEY')
headers = {"Authorization": f"Bearer {api_key}"}

# Get current hour and calculate target hour (current + 1 for upcoming market)
now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=-5)))  # EST
current_hour = now.hour
target_hour = (current_hour + 1) % 12 if current_hour < 12 else current_hour + 1
# Convert to 12-hour format
if target_hour == 0:
    target_hour = 12
target_am_pm = "PM" if target_hour >= 12 else "AM"
if target_hour > 12:
    target_hour -= 12
target_hour_str = f"{target_hour}{target_am_pm}"

# Get Fear & Greed
fg_resp = requests.get("https://api.alternative.me/fng/?limit=1")
fg = fg_resp.json()["data"][0]
fg_val = int(fg["value"])

# Get funding
coinalyze_key = os.environ.get('COINALYZE_API_KEY', '')
fund_resp = requests.get(
    "https://api.coinalyze.net/v1/funding-rate?symbols=BTCUSDT_PERP.A,ETHUSDT_PERP.A,SOLUSDT_PERP.A,XRPUSDT_PERP.A",
    headers={"api_key": coinalyze_key} if coinalyze_key else {}
)
funding = {f["symbol"]: f["value"] for f in fund_resp.json()}

coins = ["bitcoin", "ethereum", "solana", "xrp"]
month = now.strftime("%B").lower()
day = now.day

print(f"Fear & Greed: {fg_val} ({fg['value_classification']})")
print(f"Funding: BTC {funding.get('BTCUSDT_PERP.A', 0):.3f}% | ETH {funding.get('ETHUSDT_PERP.A', 0):.3f}% | SOL {funding.get('SOLUSDT_PERP.A', 0):.3f}%")
print(f"Target market: {month} {day}, {target_hour_str} ET")
print("")

for coin in coins:
    # Build query for upcoming hour market
    query = f"{coin}-up-or-down-{month}-{day}-{target_hour_str}-et"
    resp = requests.get(f"https://heyvincent.ai/api/skills/polymarket/markets?query={query}&limit=1", headers=headers)
    data = resp.json()
    
    if not data.get("data", {}).get("markets"):
        print(f"{coin.upper()}: NO MARKET ({target_hour_str})")
        continue
        
    market = data["data"]["markets"][0]
    up_price = float(market.get("outcomePrices", [0.5, 0.5])[0])
    down_price = float(market.get("outcomePrices", [0.5, 0.5])[1])
    volume = market.get("volumeNum", 0)
    liquidity = volume  # Approximate liquidity from volume
    
    # Calculate spread
    spread = abs(up_price - down_price) * 100
    
    # Calculate edge (deviation from 50%)
    edge = abs(50 - (up_price * 100))
    
    # ========== FULL CONVICTION FORMULA (HEARTBEAT.md) ==========
    # CONVICTION = (Base + Edge + Data + Structure) × Confidence
    
    # Base = 50
    conviction = 50
    
    # Edge = Market mispricing (0-40)
    edge_score = min(int(edge), 40)
    conviction += edge_score
    
    # Data = Research quality (0-25) - Crypto specific
    data_score = 0
    # Fear/Greed = +5
    if fg_val <= 25 or fg_val >= 75:
        data_score += 5
    # Funding = +5
    coin_perp = f"{coin.upper()}USDT_PERP.A" if coin != "bitcoin" else "BTCUSDT_PERP.A"
    fund = funding.get(coin_perp, 0)
    if abs(fund) > 0.005:  # Meaningful funding
        data_score += 5
    # Technicals (price vs 50%) = +5
    if up_price < 0.4 or up_price > 0.6:
        data_score += 5
    # On-chain (volume) = +5
    if volume > 10000:  # Reasonable volume
        data_score += 5
    
    conviction += data_score
    
    # Structure = Resolution clarity (0-15)
    # Crypto markets have clear resolution (Coinbase price) = +10
    structure_score = 10
    conviction += structure_score
    
    # Confidence = Time × Liquidity × Spread
    time_to_expiry = 60  # Assume 1 hour for hourly markets
    if time_to_expiry > 30:
        time_conf = 1.0
    elif time_to_expiry > 15:
        time_conf = 0.9
    else:
        time_conf = 0.7
    
    if liquidity > 20000:
        liq_conf = 1.0
    elif liquidity > 5000:
        liq_conf = 0.9
    else:
        liq_conf = 0.7
    
    if spread < 2:
        spread_conf = 1.0
    elif spread < 5:
        spread_conf = 0.9
    else:
        spread_conf = 0.8
    
    confidence = time_conf * liq_conf * spread_conf
    
    # Final conviction
    conviction = conviction * confidence
    conviction = min(max(conviction, 0), 100)
    
    # Determine action
    if edge >= 5 and conviction >= 70:
        action = ">>> AUTO INVEST"
        size = "$10" if conviction >= 85 else "$5"
    else:
        action = "PASS"
        size = ""
    
    print(f"{coin.upper()} {target_hour_str}: Edge {edge:.1f}% | Data {data_score} | Struct {structure_score} | Conf {confidence:.2f} | Conv {int(conviction)}% | {action} {size}")

print("")
print("=== FULL CONVICTION FORMULA (HEARTBEAT.md) ===")
print("CONVICTION = (Base 50 + Edge + Data + Structure) × Confidence")
print("  Edge: 0-40 (market mispricing)")
print("  Data: 0-25 (Fear/Greed + Funding + Technicals + On-chain)")
print("  Structure: ±15 (resolution clarity)")
print("  Confidence: Time × Liquidity × Spread")
print("Auto-Trade: Edge ≥5% + Conviction ≥70% = AUTO INVEST")
PYEOF