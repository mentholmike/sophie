# TOOLS.md - Sophie's Setup

> **Lightweight reference. Full API config in `context/memory/fact/api-config.md`**

## Vincent Wallet (PRIMARY TRADING)
- **Address:** `0x4e56fe13d01fd6217243020e5dcc040b021d2493`
- **Dashboard:** https://heyvincent.ai
- **Fund with:** USDC.e only (Polygon bridged)

## Key Endpoints
| Action | Endpoint |
|--------|----------|
| Balance | `/api/skills/polymarket/balance` |
| Holdings | `/api/skills/polymarket/holdings` |
| Open Orders | `/api/skills/polymarket/positions` |
| Search Markets | `/api/skills/polymarket/markets?query=<keyword>` |
| Place Bet | `/api/skills/polymarket/bet` |

## Auth
```
Authorization: Bearer $VINCENT_API_KEY
```

## Skills Available
- `vincentpolymarket` — Primary trading
- `polymarket-weather-trader` — Weather markets  
- `duckduckgo-search` — Research
- `weather` — Aviation forecasts (METAR/TAF)

---

*Full API details: `context/memory/fact/api-config.md`*
*Bet workflow: `skills/vincentpolymarket/SKILL.md`*