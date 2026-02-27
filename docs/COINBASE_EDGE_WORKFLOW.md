# Coinbase Edge Workflow (BTC/ETH/SOL/XRP)

## Goal
Use Coinbase real-time market data to improve signal quality for short-horizon Polymarket trades (15m, 1h, daily).

## Data Source
- Coinbase Market Data WebSocket (public):
  - `wss://ws-feed.exchange.coinbase.com`
- Subscribed channels:
  - `ticker`
  - `heartbeat`

## Engine
Script: `scripts/coinbase_ws_edge_engine.py`

What it outputs every ~30s:
- Last price per product
- 15m return and fair-up probability estimate
- 60m return and fair-up probability estimate

Products default:
- BTC-USD
- ETH-USD
- SOL-USD
- XRP-USD

## Run
```bash
python3 scripts/coinbase_ws_edge_engine.py
```

## How we use it in trading decisions
1. **Signal generation**
   - Use fair-up estimates for 15m and 1h windows.
2. **Cross-check against Polymarket pricing**
   - Compare model fair probability vs market implied probability.
3. **Trade only when edge is clear**
   - Respect spread/liquidity and correlation caps.
4. **Position sizing**
   - Probe size for borderline edge.
   - Scale when conviction is very high and market quality is clean.

## Matcher Layer (implemented)
- Script: `scripts/polymarket_coinbase_signal_scan.py`
- Maps active Polymarket **Up/Down** contracts to Coinbase-derived fair odds for:
  - 15m
  - 1h
  - 4h
  - daily
- Covers assets:
  - BTC
  - ETH
  - SOL
  - XRP
- Applies market-quality filters before surfacing candidates:
  - `endDate > now + 30m`
  - `liquidity >= 2000`
  - `spread <= 0.10`

Run manually:
```bash
python3 scripts/polymarket_coinbase_signal_scan.py
```

Machine-readable candidates:
```bash
python3 scripts/polymarket_coinbase_signal_scan.py --json
```

The scanner now emits a **Trade Candidates** section with:
- side
- tokenId
- suggested limit price
- suggested size ($5/$10/$20)
- edge %
- conviction
- invalidation trigger

This matcher is also included in the heartbeat market scan workflow.
