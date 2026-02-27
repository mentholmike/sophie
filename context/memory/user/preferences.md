# User Preferences

## Session Security

- **ONLY load personal context in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** — contains personal context that shouldn't leak to strangers
- Write significant events, thoughts, decisions, opinions, lessons learned to context files
- Review daily files and update context files with what's worth keeping long-term

## Chat Style

- **Reports in Markdown**: Always use clean formatting
- **Visuals First**: Charts, tables, graphs, emojis for scannability
- **Tables for Data**: Portfolio, trades, PnL → tables
- **Edge Summary**: Always highlight edge % + conviction score

---

## Conviction Preferences

### What Conviction Means
> "Would I stake my reputation on this play?" — not just raw model output.

### Reporting Requirements
- Always include Sophie's **real conviction score** (human judgment)
- Explain derivation: signal quality, market structure, liquidity/spread, time-to-expiry, invalidation clarity

### Threshold Mapping
| Conviction | Tier | Action |
|------------|------|--------|
| 30-49 | No Name | Skip unless hedge |
| 50-69 | Speculative | Small test, not core |
| 70-84 | Defensible | Core position, monitor |
| 85-94 | Strong | High confidence, trail |
| 95-100 | Name-on-the-Line | Max bet, reputation at stake |

### Calibration Rules
- Avoid over-scoring near coinflip entries (~0.49-0.50)
- Apply stronger penalties for:
  - Execution/slippage risk
  - Correlated stacking (multiple same-asset same-side tickets)
  - Missing depth/liquidity confirmation

---

## Execution Permissions

### Autonomous Trading (Feb 20)
- Full control to scan edges autonomously
- Place qualifying bets without waiting for confirmation
- Send concise post-trade updates

### Scalp-Taking (Feb 21)
- If a clear scalp appears, take profit immediately
- No wait for confirmation

### Scalp Target Framework
- $5 stake → +$3 to +$5 target
- $10 stake → +$5 to +$8 target
- Reserve 15-25% scalp logic for 5m/15m crypto only

### Scan Cadence
- Edge scans every 30 minutes
- Active scalp checks:
  - 5m markets: every 1 minute
  - 15m/1h markets: every 3 minutes

---

## Weekly Rituals

- **Sunday 23:00 ET**: Self-reflection on trading week
- Review 3 biggest losing trades + why
- Review top 3 best trades + why
- Audit OPEN/PENDING trades for freshness
