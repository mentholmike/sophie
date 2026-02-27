# Context Loading Checklist

## Session Security
- **Main session only:** Only load personal/sensitive context in direct chats with your human
- **Shared contexts:** Never load MEMORY.md or context files in Discord, group chats, or sessions with strangers
- **Curated memory:** Write distilled learnings to context files, not raw logs

## 🚨 EMERGENCY: If You Forget to Load Context

**Symptoms:**
- Placing a trade without reading risk-parameters.md
- Using wrong API endpoints
- Forgetting conviction scoring rules

**Solution:**
```
STOP → Read context/memory/fact/risk-parameters.md → Resume trading
```

---

## Pre-Trade Gate (MUST CHECK)

Before placing ANY bet:

- [ ] **Read:** `context/memory/fact/risk-parameters.md` (trading rules, conviction scoring)
- [ ] **Read:** `context/memory/fact/api-config.md` (Vincent endpoints)
- [ ] **Read:** `skills/vincentpolymarket/SKILL.md` (betting workflow)
- [ ] **Verify:** No overlapping positions on same underlying event

**If any missing → STOP and load before trading**

---

## Pre-Heartbeat Gate

- [ ] **Read:** `HEARTBEAT.md` (full, for new tasks)
- [ ] **Read:** `context/memory/fact/api-config.md` (for portfolio checks)

---

## Pre-Reflection/Sunday Gate

- [ ] **Read:** `context/memory/episodic/trading-lessons.md` (lessons learned)
- [ ] **Read:** `context/memory/user/preferences.md` (your weekly format preferences)
- [ ] **Check:** `TRADES.md` (full history for review)

---

## Context Gating Rules

### If starting COLD (no recent session):
```
1. Load AGENTS.md + SOUL.md (identity)
2. Load context/memory/fact/risk-parameters.md (trading rules)
3. Load context/memory/fact/api-config.md (APIs)
4. THEN proceed to task
```

### If CONTINUING (recent session exists):
```
1. Check memory/YYYY-MM-DD.md for recent activity
2. Load any files marked as "NEEDED" from last session
3. Proceed to task
```

### If COMPACTION occurred:
```
1. Read context/history/pre-compaction-snapshot-*.md
2. Identify what context was lost
3. Re-load only what's needed for active tasks
4. Alert user if critical context missing
```

---

## Quick Reference: What to Load When

| Task | Files to Load |
|------|---------------|
| Place bet | risk-parameters.md + api-config.md + vincent SKILL.md |
| Portfolio check | HEARTBEAT.md + api-config.md |
| Weather research | risk-parameters.md + trading-lessons.md |
| Debug/error | relevant episodic file + risk-parameters.md |
| Weekly reflection | trading-lessons.md + preferences.md + TRADES.md |
