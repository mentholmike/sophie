# Task Queue — Sophie’s Autonomy Hub

## Ready

- [ ] *(none)*

## In Progress

- [ ] *(none)*

## Blocked

- [ ] **Run drift tracker check** (conviction drift >15% after entry) — requires per-trade `trade_id` + `current_conviction` inputs

## Done

- [x] Verify wallet balance ≥ $10 — balance $86.17 (OK)
- [x] Audit portfolio for any resolved YES markets pending redemption — 10 redeemable positions detected (alert)
- [x] **Check unredeemed positions >12h old** (flag and alert) — 10 redeemable positions still pending (alert)
- [x] Run overnight scan (23:00-08:00 EST) and log trades to morning summary — completed 23:48 ET, artifacts saved in reports/market-scan/
- [x] Review open limit orders and cancel if stale — 1 LIVE ETH GTC order checked, not stale yet; kept active
- [x] **Run loss tracker check** (check for 3 losses in 6h) — 0 losses (OK)
- [x] Check BTC hourly markets and compare with market structure/price action signals; BTC hourly market snapshot captured
- [x] Scan for weather markets with >5% edge (METAR/TAF + Polymarket odds) — no qualifying edge executed this cycle
- [x] Memory Manager structure initialized (episodic/semantic/procedural)
- [x] HEARTBEAT.md updated with agent autonomy flow
- [x] Auto-trade rules finalised with conviction thresholds & size
- [x] Night scan protocol added: report trades placed after 8 AM EST
- [x] CryptoQuant helper script created (scripts/cryptoquant.sh)
- [x] Edge query CLI helper (scripts/edge-query.sh)
- [x] Loss tracker script (scripts/loss-tracker.sh)
- [x] Drift tracker script (scripts/drift-tracker.sh)
- [x] Conviction calculation framework documented
- [x] Risk controls: loss threshold, drawdown monitor, auto-rebalance
- [x] Weekly loss report cron scheduled
- [x] Unredeemed tracker logic in portfolio checks
