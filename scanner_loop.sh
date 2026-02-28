#!/bin/bash
API_KEY="ssk_f3aa322bd7c98a60d1475e25534ce5e4cfb4ac60e4b994be0c026f39820824ae"
LOG_FILE="memory/scanner-2026-02-27.md"
CYCLES=24
SLEEP=300

echo "# Scanner Log - 2026-02-27" > "$LOG_FILE"

# Get balance
BALANCE=$(curl -s -X GET "https://heyvincent.ai/api/skills/polymarket/balance" -H "Authorization: Bearer $API_KEY" | jq -r '.data.balance // "error"')
echo "## Balance at start: $"$BALANCE >> "$LOG_FILE"
echo "## Cycles" >> "$LOG_FILE"

for i in $(seq 1 $CYCLES); do
    TIMESTAMP=$(date "+%H:%M")
    echo "### $TIMESTAMP - Cycle $i" >> "$LOG_FILE"
    echo "Checking markets..." >> "$LOG_FILE"
    
    # Get current crypto prices
    BTC=$(curl -s "https://api.coinbase.com/v2/prices/BTC-USD/spot" | jq -r '.data.amount')
    ETH=$(curl -s "https://api.coinbase.com/v2/prices/ETH-USD/spot" | jq -r '.data.amount')
    SOL=$(curl -s "https://api.coinbase.com/v2/prices/SOL-USD/spot" | jq -r '.data.amount')
    XRP=$(curl -s "https://api.coinbase.com/v2/prices/XRP-USD/spot" | jq -r '.data.amount')
    
    echo "- BTC: \$$BTC" >> "$LOG_FILE"
    echo "- ETH: \$$ETH" >> "$LOG_FILE"
    echo "- SOL: \$$SOL" >> "$LOG_FILE"  
    echo "- XRP: \$$XRP" >> "$LOG_FILE"
    
    # Check key markets
    # BTC $66k Feb 28
    BTC66=$(curl -s -X GET 'https://heyvincent.ai/api/skills/polymarket/markets?query=bitcoin%20above%20%2466000%20feb%2028&limit=5' -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "- BTC $66k Feb 28: $BTC66" >> "$LOG_FILE"
    
    # ETH $1900 Feb 28
    ETH1900=$(curl -s -X GET 'https://heyvincent.ai/api/skills/polymarket/markets?query=ethereum%20above%20%241900%20feb%2028&limit=5' -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "- ETH $1900 Feb 28: $ETH1900" >> "$LOG_FILE"
    
    # SOL $80 Feb 28
    SOL80=$(curl -s -X GET 'https://heyvincent.ai/api/skills/polymarket/markets?query=solana%20above%20%2480%20feb%2028&limit=5' -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "- SOL $80 Feb 28: $SOL80" >> "$LOG_FILE"
    
    # XRP $1.40 Feb 28
    XRP140=$(curl -s -X GET 'https://heyvincent.ai/api/skills/polymarket/markets?query=xrp%20above%20%241.40%20feb%2028&limit=5' -H "Authorization: Bearer $API_KEY" | jq -r '.data.markets[0].outcomePrices[0] // "N/A"')
    echo "- XRP $1.40 Feb 28: $XRP140" >> "$LOG_FILE"
    
    # Check for edge (manually based on price vs probability)
    echo "Edge check..." >> "$LOG_FILE"
    
    # SOL check - if price above $80 and market < 75%, that's edge
    if (( $(echo "$SOL > 80" | bc -l) )) && [ "$SOL80" != "N/A" ] && (( $(echo "$SOL80 < 0.75" | bc -l) )); then
        echo ">>> SOL $80: Price above target, market at $SOL80 - potential edge!" >> "$LOG_FILE"
    fi
    
    echo "" >> "$LOG_FILE"
    
    if [ $i -lt $CYCLES ]; then
        sleep $SLEEP
    fi
done

echo "Scanner complete at $(date)" >> "$LOG_FILE"
