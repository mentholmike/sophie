# HEARTBEAT.md

> **Lightweight reference. Full content in `context/` folder.**

## Memory Health Check (Every Heartbeat)
1. Verify `memory/YYYY-MM-DD.md` exists
2. Check `context/memory/fact/` has required files
3. Check for compaction events → read pre-compaction snapshot if needed

## Heartbeat Checklist (Lightweight - Feb 24, 2026)

**Subagent Check:**
- Verify 2 active: `subagents(action=list)`
- Expected: scanner + scalper running
- **If scanner missing → spawn new scanner**
- **If scalper missing → spawn new scalper**
- Check log freshness: `memory/scanner-YYYY-MM-DD.md` (>30min stale = alert)

**Auto-Restart (CRITICAL):**
- If any subagent is missing or done → spawn new one immediately
- Don't wait — keep the system running 24/7

**Hourly Status Update (Every 6 heartbeats ~30 min):**
- Check subagent logs for recent activity
- Report: balance, open positions, recent trades
- If scanner found opportunities → note them
- If scalper took profit/loss → note them

**Periodic Checks (Delegated to Subagents):**
- Market scanning → scanner handles
- Position monitoring → scalper handles
- Balance check → use Vincent API (`/balance`)

**DO NOT Re-scan Markets in Heartbeat** scanners do all the heavy lifting

### Spawn Schedule
- Run 2-hour sessions
- Respawn after timeout
---
