#!/bin/bash
API_KEY="ssk_f3aa322bd7c98a60d1475e25534ce5e4cfb4ac60e4b994be0c026f39820824ae"
LOG_FILE="memory/scanner-2026-02-27.md"

# Initialize log
echo "# Scanner Log - 2026-02-27" > "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Get balance
BALANCE=$(curl -s -X GET "https://heyvincent.ai/api/skills/polymarket/balance" -H "Authorization: Bearer $API_KEY" | jq -r '.data.balance // "error"')
echo "## Starting Balance: \$$BALANCE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Run 24 cycles (2 hours / 5 min = 24)
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24; do
    TIMESTAMP=$(date "+%H:%M")
    echo "### Cycle $i - $TIMESTAMP" >> "$LOG_FILE"
    
    # Get live prices
    BTC=$(curl -s "https://api.coinbase.com/v2/prices/BTC-USD/spot" | jq -r '.data.amount')
    ETH=$(curl -s "https://api.coinbase.com/v2/prices/ETH-USD/spot" | jq -r '.data.amount')
    SOL=$(curl -s "https://api.coinbase.com/v2/prices/SOL-USD/spot" | jq -r '.data.amount')
    XRP=$(curl -s "https://api.coinbase.com/v2/prices/XRP-USD/spot" | jq -r '.data.amount')
    
    echo "Prices: BTC=$$BTC ETH=$$ETH SOL=$$SOL XRP=$$XRP" >> "$LOG_FILE"
    
    # Search for target markets - using more specific queries
    # BTC $66k Feb 28 - use exact price in query
    BTC66=$(curl -s -X GET "https://heyvincent.ai/api/skills/polymarket/markets?query=bitcoin%20be%20above%20%2466000%20february%2028&limit=3" -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "BTC>\$66k: $$BTC66" >> "$LOG_FILE"
    
    # ETH $1900 Feb 28
    ETH1900=$(curl -s -X GET "https://heyvincent.ai/api/skills/polymarket/markets?query=ethereum%20be%20above%20%241900%20february%2028&limit=3" -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "ETH>\$1900: $$ETH1900" >> "$LOG_FILE"
    
    # SOL $85 Feb 28  
    SOL85=$(curl -s -X GET "https://heyvincent.ai/api/skills/polymarket/markets?query=solana%20be%20above%20%2485%20february%2028&limit=3" -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "SOL>\$85: $$SOL85" >> "$LOG_FILE"
    
    # XRP $1.40 Feb 28
    XRP140=$(curl -s -X GET "https://heyvincent.ai/api/skills/polymarket/markets?query=xrp%20be%20above%20%241.40%20february%2028&limit=3" -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "XRP>\$1.40: $$XRP140" >> "$LOG_FILE"
    
    echo "" >> "$LOG_FILE"
    
    # Sleep 5 minutes between cycles
    if [ $i -lt 24 ]; then
        sleep 300
    fi
done

echo "Scanner complete at $(date)" >> "$LOG_FILE"
