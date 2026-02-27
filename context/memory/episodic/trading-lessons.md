# Trading Lessons - Feb 2026

## Key Insights

### Weather vs Crypto
- Weather markets offer clearer edges than crypto
- Aviation-grade data (METAR, NOAA hourly) gives significant edge vs retail forecasts
- NYC temp market had 17% edge on Feb 16 2026

### Vincent API Rules
1. Vincent is the ONLY source for portfolio data — never query Polymarket directly
2. Token ID order: `tokenIds[0]` = Yes, `tokenIds[1]` = No
3. Fund with USDC.e only (Polygon bridged), not native USDC

### Weather Resolution
- 'Highest temp on DATE' = Full calendar day max (Wunderground)
- Market `endDate` ~7AM ET next day (captures finalize), but hottest ~2-4PM prior
- Don't assume morning end resolves low
- Finalize: Wunderground post-24h

---

## Critical Mistakes

### ❌ Overlapping Timeframe Bets (Feb 18)
**Problem:** Placed 7 separate Elon tweet count bets across overlapping windows
- Feb 10-17 (200-219)
- Feb 13-20 (100-119, 200-219, 260-279)
- Feb 16-18 (65-89, 115-139)

**All lost when Elon exceeded 200 tweets/day.**

**Fix:** Never place multiple bets on overlapping timeframes of same event.

### ❌ Weather Market End Time (Feb 18)
**Problem:** NYC 38-39°F Feb 18 ended at 7AM ET (when temp was ~36°F), not 24h
- "Daily high" should span full day (2-4PM is hottest)

**Fix:** Always verify end time aligns with metric being measured.

### ❌ Conviction Drift Not Monitored (Feb 18)
**Problem:** Position went from 9% → 2.6% price without alert
- Drift was 64%, no system flagged it

**Fix:** Track conviction changes >15%, trigger alerts

---

## Weather Market Edge Tools

Aviation-grade (retail doesn't use these):
- **METAR:** Current conditions
- **TAF:** 24-30hr forecasts  
- **PIREPs:** Pilot reports
- **SIGMET/AIRMET:** Severe weather advisories
- **GFS/ECMWF:** Model runs
- **Aviation Weather Center:** aviationweather.gov

---

## Market Status Meanings

| Status | Meaning |
|--------|---------|
| OPEN | Still has time remaining |
| PENDING | Position pending resolution |
| CLOSED | Market resolved (YES or NO) |
| RESOLVED | Same as CLOSED, known outcome |

**Important:** A market that hasn't resolved is NOT a loss — it's just underwater based on tracker data.
