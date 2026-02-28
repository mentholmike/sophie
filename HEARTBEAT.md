# HEARTBEAT.md

> Simple heartbeat: check subagents, restart if needed.

## Checklist

1. `subagents(action=list)` — verify scanner + scalper running
2. If either missing → spawn new one immediately (instructions in `context/memory/fact/api-config.md`)
3. If both running → `HEARTBEAT_OK`

That's it. Subagents handle all trading logic.
