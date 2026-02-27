#!/usr/bin/env python3
import json
import os
import re
import urllib.request
from typing import Dict, Any

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
TRADES_PATH = os.path.join(WORKSPACE, "TRADES.md")
CONV_PATH = os.path.join(WORKSPACE, "data", "conviction_live.json")
SCAN_PATH = os.path.join(WORKSPACE, "reports", "market-scan", "coinbase-polymarket-latest.json")
CRED_PATH = os.path.expanduser("~/.openclaw/credentials/agentwallet/cmloigqm30003i8r0hjqdc5wr.json")


def load_api_key() -> str:
    env = os.getenv("VINCENT_API_KEY", "").strip()
    if env:
        return env
    if os.path.exists(CRED_PATH):
        with open(CRED_PATH, "r", encoding="utf-8") as f:
            j = json.load(f)
        return (j.get("apiKey") or j.get("key") or j.get("api_key") or "").strip()
    return ""


def http_json(url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def parse_entry_conv_map() -> Dict[str, tuple]:
    if not os.path.exists(TRADES_PATH):
        return {}
    txt = open(TRADES_PATH, "r", encoding="utf-8").read()
    out = {}
    # Parse markdown rows with token id + "Conviction (Entry→Now)" column like "81 → 81"
    for line in txt.splitlines():
        if not line.startswith("| 20"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 13:
            continue
        token = cols[1]
        status = cols[8].upper()
        conv_col = cols[11]
        if "OPEN" not in status and "PENDING" not in status and "ORDER" not in status:
            continue
        m = re.search(r"(\d+(?:\.\d+)?)\s*→\s*(\d+(?:\.\d+)?)", conv_col)
        if m:
            out[token] = (float(m.group(1)), float(m.group(2)))
    return out


def load_scan_map() -> Dict[str, float]:
    if not os.path.exists(SCAN_PATH):
        return {}
    try:
        with open(SCAN_PATH, "r", encoding="utf-8") as f:
            j = json.load(f)
        out = {}
        for c in j.get("tradeCandidates", []):
            tid = str(c.get("tokenId", "")).strip()
            conv = c.get("conviction")
            if tid and isinstance(conv, (int, float)):
                out[tid] = float(conv)
        return out
    except Exception:
        return {}


def conviction_score(edge: float, spread: float, liq: float) -> int:
    """Heuristic score: edge dominates, spread penalizes."""
    liq_bonus = 5 if liq >= 10000 else (2 if liq >= 5000 else 0)
    score = 50 + (edge * 260) - (spread * 120) + liq_bonus
    return int(max(0, min(99, round(score))))


def main() -> int:
    api_key = load_api_key()
    if not api_key:
        print(json.dumps({"ok": False, "error": "missing_api_key"}))
        return 1

    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json", "User-Agent": "SophieConvictionUpdater/1.0"}
    holdings = http_json("https://heyvincent.ai/api/skills/polymarket/holdings", headers)
    rows = holdings.get("data", {}).get("holdings", [])

    entry_map = parse_entry_conv_map()
    scan_map = load_scan_map()

    if os.path.exists(CONV_PATH):
        try:
            cur_file = json.load(open(CONV_PATH, "r", encoding="utf-8"))
        except Exception:
            cur_file = {}
    else:
        cur_file = {}

    out = {}
    for h in rows:
        token = str(h.get("tokenId", "")).strip()
        if not token:
            continue
        if h.get("redeemable") is True:
            continue
        if float(h.get("currentPrice", 0) or 0) in (0.0, 1.0):
            continue

        entry_vals = entry_map.get(token)
        prev = cur_file.get(token, {}) if isinstance(cur_file.get(token, {}), dict) else {}
        
        # Get entry conviction from entry_map or fallback
        entry_conv = entry_vals[0] if entry_vals else prev.get("entry")
        if entry_conv is None:
            entry_conv = 75.0  # conservative fallback

        # Get current conviction from scan_map or previous value
        current_conv = scan_map.get(token)
        if current_conv is None:
            current_conv = prev.get("current", entry_conv)

        # Only update timestamp if conviction actually changed from previous
        was_updated = prev.get("updatedAt")
        if current_conv != entry_conv:
            # Conviction drifted - update timestamp
            updated_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
        elif was_updated is None:
            # First time tracking
            updated_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
        else:
            # Keep original timestamp if conviction unchanged
            updated_at = was_updated

        out[token] = {
            "entry": float(entry_conv),
            "current": float(current_conv),
            "market": h.get("marketTitle", ""),
            "updatedAt": updated_at,
        }

    os.makedirs(os.path.dirname(CONV_PATH), exist_ok=True)
    with open(CONV_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(json.dumps({"ok": True, "tracked": len(out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
