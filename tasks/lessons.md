# Lessons & Self-Improvement Log

## 2026-02-22 — Workflow Orchestration Guidelines Added

### New Guidelines Integrated
- **Plan Node Default**: Enter plan mode for 3+ step tasks, verify before execution
- **Subagent Strategy**: Offload research to subagents, keep main context clean
- **Self-Improvement Loop**: Update lessons.md after corrections, prevent repeat mistakes
- **Verification Before Done**: Prove it works, ask "Would a staff engineer approve?"
- **Demand Elegance**: Challenge own work, balance pragmatism vs over-engineering
- **Autonomous Bug Fixing**: Just fix it, no hand-holding required

### Task Management
- Plan First: Write to tasks/todo.md
- Verify: Get alignment before execution
- Track: Mark items complete
- Document: Add review sections
- Capture: Update lessons.md after major learnings

### Core Principles Applied
- Simplicity First
- No Laziness (root cause)
- Minimal Impact
- Observability Matters
- Graceful Degradation
- Human-in-the-Loop Gates for high-risk

---

## Prior Lessons

### 2026-02-18 — Overlapping Bets Mistake
- Never place multiple bets on overlapping timeframes of same event
- Added to HEARTBEAT.md: "Review overlapping bets" weekly

### 2026-02-18 — Weather Market Timing
- Verify endDate aligns with metric (daily high = 24h span)
- Ask before trading if timing unclear

### 2026-02-18 — Conviction Drift
- Track conviction changes >15%, trigger alerts
- Position closes when conviction drops significantly

### 2026-02-22 — Low-Liquidity Weather Markets
- Never enter thin weather range markets (<$2k volume)
- Cannot exit positions when liquidity is too low
- Lesson: Check volume BEFORE entering — stuck capital = forced hold

### 2026-02-22 — Slippage Execution
- Miami 78°F+ filled at 0.86% vs displayed 0.35% — 2.5x slippage
- Use limit orders at displayed price, not market orders
- Check "delayed" status carefully before assuming execution

### 2026-02-23 — Weather Forecast Timing
- Forecasts shift overnight (Miami: 79°F → 70°F)
- Enter weather positions late night (11PM-2AM) when models stabilize
- Re-check morning (6-9AM) before final entry
- Never enter based on afternoon forecast alone
