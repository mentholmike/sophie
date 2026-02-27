#!/bin/bash
# loss-tracker.sh - Track losses and trigger alerts
# Usage:
#   ./loss-tracker.sh init      # Create/reset loss log
#   ./loss-tracker.sh log <pnl> # Log a trade PnL
#   ./loss-tracker.sh check     # Check if 3 losses in 6h, return alert if true
#   ./loss-tracker.sh reset     # Reset loss count

LOG_FILE="$HOME/.openclaw/workspace/memory/loss-log.jsonl"

# Ensure log file exists
touch "$LOG_FILE"

case "$1" in
    init)
        > "$LOG_FILE"
        echo "✅ Loss tracker initialized"
        ;;
    log)
        PNL="$2"
        if [ -z "$PNL" ]; then
            echo "❌ Error: PnL value required"
            exit 1
        fi
        echo "{\"timestamp\":$(date +%s),\"pnl\":$PNL}" >> "$LOG_FILE"
        echo "✅ Logged PnL: $PNL"
        ;;
    check)
        NOW=$(date +%s)
        SIX_HOURS=$((6 * 60 * 60))
        THRESHOLD=$(($NOW - SIX_HOURS))
        
        # Count recent losses (PnL ≤ -5%)
        LOSS_COUNT=0
        while IFS= read -r line; do
            TIMESTAMP=$(echo "$line" | jq -r '.timestamp // 0')
            PNL=$(echo "$line" | jq -r '.pnl // 0')
            if [ "$TIMESTAMP" -ge "$THRESHOLD" ] && [ "$(echo "$PNL <= -5" | bc -l)" -eq 1 ]; then
                LOSS_COUNT=$((LOSS_COUNT + 1))
            fi
        done < "$LOG_FILE"
        
        if [ "$LOSS_COUNT" -ge 3 ]; then
            echo "⚠️  LOSS THRESHOLD ALERT: $LOSS_COUNT losses in 6h → pause auto-trades"
            echo "Resume with: /resume_trades"
        else
            echo "✅ Loss count: $LOSS_COUNT (threshold: 3)"
        fi
        ;;
    reset)
        > "$LOG_FILE"
        echo "✅ Loss tracker reset"
        ;;
    *)
        echo "Usage: $0 {init|log|check|reset}"
        echo ""
        echo "Commands:"
        echo "  init  - Initialize/reset loss log"
        echo "  log   - Log a trade PnL (e.g., -5.5)"
        echo "  check - Check if 3+ losses in 6h"
        echo "  reset - Clear loss log"
        exit 1
        ;;
esac
