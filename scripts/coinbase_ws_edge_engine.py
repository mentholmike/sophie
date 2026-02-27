#!/usr/bin/env python3
"""
Coinbase WebSocket edge engine (public feed, no auth).

Streams ticker data for BTC/ETH/SOL/XRP from Coinbase Exchange and emits
simple directional probabilities for 15m and 1h horizons using recent
momentum + realized volatility.

Usage:
  python3 scripts/coinbase_ws_edge_engine.py

Optional env vars:
  PRODUCTS=BTC-USD,ETH-USD,SOL-USD,XRP-USD
  WS_URI=wss://ws-feed.exchange.coinbase.com
"""

import asyncio
import json
import math
import os
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict
import urllib.request

try:
    import websockets  # type: ignore
except Exception:
    websockets = None

WS_URI = os.getenv("WS_URI", "wss://ws-feed.exchange.coinbase.com")
PRODUCTS = [p.strip() for p in os.getenv("PRODUCTS", "BTC-USD,ETH-USD,SOL-USD,XRP-USD").split(",") if p.strip()]

# Keep up to 2h of second-level snapshots
WINDOW_SECS = 2 * 60 * 60
EMIT_EVERY_SECS = 30


@dataclass
class Tick:
    ts: float
    px: float


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def find_price_at_or_before(ticks: Deque[Tick], target_ts: float) -> float:
    # Linear reverse scan is fine for short deques.
    for t in reversed(ticks):
        if t.ts <= target_ts:
            return t.px
    return ticks[0].px


def calc_return(ticks: Deque[Tick], lookback_sec: int) -> float:
    if len(ticks) < 2:
        return 0.0
    now = ticks[-1].ts
    p_now = ticks[-1].px
    p_then = find_price_at_or_before(ticks, now - lookback_sec)
    if p_then <= 0:
        return 0.0
    return (p_now / p_then) - 1.0


def calc_realized_vol(ticks: Deque[Tick], lookback_sec: int = 3600) -> float:
    if len(ticks) < 10:
        return 0.0
    now = ticks[-1].ts
    series = [t for t in ticks if t.ts >= now - lookback_sec]
    if len(series) < 10:
        return 0.0
    rets = []
    for i in range(1, len(series)):
        p0 = series[i - 1].px
        p1 = series[i].px
        if p0 > 0 and p1 > 0:
            rets.append(math.log(p1 / p0))
    if len(rets) < 5:
        return 0.0
    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / max(1, len(rets) - 1)
    # Per-tick vol, scaled to rough hourly vol.
    return math.sqrt(var * max(1, len(rets)))


def fair_up_probability(ticks: Deque[Tick], horizon_sec: int) -> float:
    # Simple model: z-score of momentum over volatility -> probability.
    r = calc_return(ticks, horizon_sec)
    vol = max(calc_realized_vol(ticks, 3600), 1e-6)
    z = r / vol
    # Dampening factor to avoid overconfidence in noisy microstructure.
    return sigmoid(0.85 * z)


def trim_old(ticks: Deque[Tick]) -> None:
    cutoff = time.time() - WINDOW_SECS
    while ticks and ticks[0].ts < cutoff:
        ticks.popleft()


def print_snapshot(book: Dict[str, Deque[Tick]]) -> None:
    print("\n=== EDGE SNAPSHOT ===")
    for p in PRODUCTS:
        ticks = book.get(p)
        if not ticks:
            continue
        px = ticks[-1].px
        r15 = calc_return(ticks, 15 * 60)
        r60 = calc_return(ticks, 60 * 60)
        p15 = fair_up_probability(ticks, 15 * 60)
        p60 = fair_up_probability(ticks, 60 * 60)
        print(
            f"{p:8s} px={px:,.4f} | "
            f"ret15={r15*100:+.2f}% fairUp15={p15*100:.1f}% | "
            f"ret60={r60*100:+.2f}% fairUp60={p60*100:.1f}%"
        )


def http_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; SophieEdgeEngine/1.0)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def poll_once(book: Dict[str, Deque[Tick]]) -> None:
    now = time.time()
    for product in PRODUCTS:
        # REST fallback using Coinbase spot endpoint.
        url = f"https://api.coinbase.com/v2/prices/{product}/spot"
        try:
            j = http_json(url)
            px = float(j["data"]["amount"])
        except Exception:
            continue
        ticks = book[product]
        ticks.append(Tick(ts=now, px=px))
        trim_old(ticks)


async def run_ws() -> None:
    book: Dict[str, Deque[Tick]] = defaultdict(deque)
    sub = {"type": "subscribe", "product_ids": PRODUCTS, "channels": ["ticker"]}

    print(f"Connecting to {WS_URI}")
    print(f"Products: {', '.join(PRODUCTS)}")

    last_emit = 0.0
    while True:
        try:
            async with websockets.connect(WS_URI, ping_interval=20, ping_timeout=20) as ws:
                await ws.send(json.dumps(sub))
                print("Subscribed.")
                async for raw in ws:
                    msg = json.loads(raw)
                    if msg.get("type") == "ticker":
                        product = msg.get("product_id")
                        px_str = msg.get("price")
                        if product and px_str:
                            try:
                                px = float(px_str)
                                ticks = book[product]
                                ticks.append(Tick(ts=time.time(), px=px))
                                trim_old(ticks)
                            except Exception:
                                pass
                    if time.time() - last_emit >= EMIT_EVERY_SECS:
                        last_emit = time.time()
                        print_snapshot(book)
        except Exception as e:
            print(f"WS error: {e}. Reconnecting in 2s...")
            await asyncio.sleep(2)


async def run_polling() -> None:
    book: Dict[str, Deque[Tick]] = defaultdict(deque)
    print("websockets package not found; running REST polling fallback.")
    print(f"Products: {', '.join(PRODUCTS)}")
    while True:
        poll_once(book)
        print_snapshot(book)
        await asyncio.sleep(EMIT_EVERY_SECS)


if __name__ == "__main__":
    if websockets is None:
        asyncio.run(run_polling())
    else:
        asyncio.run(run_ws())
