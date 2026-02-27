# HEARTBEAT.md

> **Lightweight reference. Full content in `context/` folder.**

## Session Startup
```bash
cd ~/.openclaw/workspace && git pull origin main
```

## Git Workflow
- Branch: `main`
- Commit types: `feat:`, `fix:`, `update:`, `docs:`, `refactor:`, `chore:`
- **Never commit secrets** — use `.gitignore`

## Memory Health Check (Every Heartbeat)
1. Verify `memory/YYYY-MM-DD.md` exists
2. Check `context/memory/fact/` has required files
3. Check for compaction events → read pre-compaction snapshot if needed

## Context Loading Strategy

| Task | Files to Load |
|------|---------------|
| Trading | `context/memory/fact/risk-parameters.md` + `api-config.md` |
| Heartbeat | `HEARTBEAT.md` (this file) + `context/memory/fact/api-config.md` |
| Weekly Reflection | `context/memory/episodic/trading-lessons.md` + `preferences.md` |

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

**DO NOT Re-scan Markets in Heartbeat** — scanner handles this.

## Subagent System

### Scanner
- Scan: 5 min intervals
- Trigger: Conviction ≥70% + Edge ≥5%
- Size: $5 (70-84%), $10 (85%+)
- Use: MARKET orders only

### Scalper
- Monitor: 2 min intervals
- Exit: +7.3% to +15% → sell 70%, +15%+ → sell all, -35% → hard stop
- Use: MARKET orders only

### Spawn Schedule
- Run 2-hour sessions
- Respawn after timeout

## Key Rules

- **Min edge:** 5%
- **Max position:** $25
- **Auto-trade:** Conviction ≥70% + Edge ≥5%
- **Loss alert:** 3 losses in 6h → pause

## Notifications
- Telegram notifications enabled for: new trades, profit exits, max profit, stop losses

---

*For full trading rules, see `context/memory/fact/risk-parameters.md`*
*For API details, see `context/memory/fact/api-config.md`*