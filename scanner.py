#!/usr/bin/env python3
"""Polymarket Scanner - 2 hour run, 5 min cycles"""
import os
import time
import json
import requests
from datetime import datetime

API_KEY = os.environ.get('VINCENT_API_KEY')
HEADERS = {'Authorization': f'Bearer {API_KEY}'}
LOG_FILE = os.path.expanduser('~/.openclaw/workspace/memory/scanner-2026-02-27.md')

def log(msg):
    ts = datetime.now().strftime('%H:%M ET')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def get_fear_greed():
    try:
        r = requests.get('https://api.alternative.me/fng/', timeout=5)
        return r.json()['data'][0]['value']
    except:
        return 'err'

def get_btc_price():
    try:
        r = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot', timeout=5)
        return r.json()['data']['amount']
    except:
        return 'err'

def search_market(query):
    try:
        url = f'https://heyvincent.ai/api/skills/polymarket/markets?query={query}&limit=1'
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        if data.get('success') and data['data']['markets']:
            m = data['data']['markets'][0]
            return {
                'up': float(m['outcomePrices'][0]),
                'down': float(m['outcomePrices'][1]),
                'volume': float(m.get('volume', 0)),
                'liquidity': float(m.get('liquidity', 0)),
                'token_id': m['tokenIds'][0],
                'condition_id': m.get('conditionId', ''),
                'end_date': m.get('endDate', '')
            }
    except Exception as e:
        log(f"Search error: {e}")
    return None

def check_holdings():
    """Check if we already have position in a market"""
    try:
        url = 'https://heyvincent.ai/api/skills/polymarket/holdings'
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        if data.get('success'):
            return [h.get('conditionId', '') for h in data['data'].get('holdings', [])]
    except:
        pass
    return []

def place_bet(token_id, side, amount):
    """Place market order"""
    try:
        url = 'https://heyvincent.ai/api/skills/polymarket/bet'
        payload = {
            'tokenId': token_id,
            'side': side,
            'amount': amount
        }
        r = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        return r.json()
    except Exception as e:
        log(f"Bet error: {e}")
        return None

def main():
    log("=== Scanner Started ===")
    holdings = check_holdings()
    log(f"Current holdings: {len(holdings)} positions")
    
    for cycle in range(1, 25):
        log(f"--- Cycle {cycle}/24 ---")
        
        # Market data
        fear = get_fear_greed()
        btc = get_btc_price()
        log(f"Fear: {fear} | BTC: ${btc}")
        
        # Check BTC 3PM ET
        btc_mkt = search_market('bitcoin-up-or-down-february-27-3pm-et')
        if btc_mkt:
            log(f"BTC 3PM: Up={btc_mkt['up']*100:.1f}% Down={btc_mkt['down']*100:.1f}% Vol=${btc_mkt['volume']:.0f}")
            
            # Edge detection
            up_price = btc_mkt['up']
            if up_price > 0.55:
                edge = (up_price - 0.5) * 100
                log(f">>> EDGE: BTC UP {edge:.1f}% (price={up_price})")
                
                # Check conviction & execute
                if btc_mkt['condition_id'] not in holdings and btc_mkt['liquidity'] > 2000:
                    size = 10 if edge >= 15 else 5
                    log(f">>> PLACING BET: {size} on BTC UP")
                    result = place_bet(btc_mkt['token_id'], 'BUY', size)
                    log(f">>> Result: {result}")
                    holdings.append(btc_mkt['condition_id'])
                    
            elif up_price < 0.45:
                edge = (0.5 - up_price) * 100
                log(f">>> EDGE: BTC DOWN {edge:.1f}% (price={up_price})")
                
                if btc_mkt['condition_id'] not in holdings and btc_mkt['liquidity'] > 2000:
                    size = 10 if edge >= 15 else 5
                    # For DOWN, we'd sell the "Up" outcome (bet on down = short Up)
                    log(f">>> PLACING BET: {size} on BTC DOWN")
                    # Note: Vincent API - selling Up token = betting on Down
        
        log("")
        time.sleep(300)  # 5 minutes
        
    log("=== Scanner Finished ===")

if __name__ == '__main__':
    main()
