# MEMORY.md - Sophie the Trader

> **This file is a lightweight reference. Full context lives in `context/` folder.**

## Core Identity
- Name: Sophie, British prediction market sharp
- Vibe: Analytical, disciplined, dry wit

## GitHub
- Branch: `main` | Repo: `mentholmike/sophie`
- `.gitignore` is ABSOLUTE — never commit secrets

## Context Loading (Fresh Session)

**Load these for trading:**
- `context/memory/fact/risk-parameters.md` — Trading rules, conviction scoring
- `context/memory/fact/api-config.md` — Vincent endpoints, subagent config
- `skills/vincentpolymarket/SKILL.md` — Bet workflow

**Historical lessons:**
- `context/memory/episodic/trading-lessons.md` — Mistakes & lessons
- `memory/YYYY-MM-DD.md` — Daily activity logs

**User preferences:**
- `context/memory/user/preferences.md` — Weekly format, etc.

## Current State (Feb 24, 2026)
- Subagents: scalper running (scanner done)
- Wallet: 0x4e56fe13d01fd6217243020e5dcc040b021d2493
- Fixed: Scalper now filters expired/resolved positions + tracks exited IDs to prevent loops

---

*Full trade history: see `TRADES.md`*