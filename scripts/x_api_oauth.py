#!/usr/bin/env python3
"""
X API OAuth Helper - Generate Bearer Token from OAuth 1.0a credentials
Then use Bearer Token with v2 API endpoints (Essential tier compatible)
"""
import json
import sys
import os
import base64
import urllib.request
import urllib.parse

def load_creds():
    creds_file = os.path.expanduser("~/.openclaw/workspace/.x_api_creds")
    with open(creds_file) as f:
        return json.load(f)

def get_bearer_token():
    """Exchange OAuth 1.0a credentials for Bearer Token via oauth2/token"""
    creds = load_creds()
    
    # Encode credentials as Basic Auth
    credentials = f"{creds['consumerKey']}:{creds['consumerSecret']}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    req = urllib.request.Request(
        "https://api.twitter.com/oauth2/token",
        data=b"grant_type=client_credentials",
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data.get("access_token")
    except urllib.error.HTTPError as e:
        error = json.loads(e.read().decode())
        return {"error": error}

def fetch_tweets_v2(user_id, since_id=None, max_results=100):
    """Fetch tweets using v2 API with Bearer Token"""
    bearer = get_bearer_token()
    if isinstance(bearer, dict) and "error" in bearer:
        return bearer
    
    # Build URL
    params = {
        "tweet.fields": "created_at,referenced_tweets",
        "exclude": "replies",
        "max_results": max(max_results, 5)  # v2 requires 5-100
    }
    
    if since_id:
        params["since_id"] = since_id
    
    query = urllib.parse.urlencode(params)
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?{query}"
    
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {bearer}"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())

def filter_by_window(data, start_time, end_time):
    """Filter tweets by time window and count them"""
    from datetime import datetime
    
    count = 0
    newest_in_window = None
    
    for tweet in data.get('data', []):
        created_str = tweet.get('created_at', '')
        if created_str:
            try:
                dt = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                tweet_time = int(dt.timestamp())
                
                if start_time <= tweet_time <= end_time:
                    count += 1
                    if newest_in_window is None or tweet_time > newest_in_window:
                        newest_in_window = tweet_time
            except:
                pass
    
    return count

def get_newest_timestamp(data):
    """Get the newest tweet timestamp from data"""
    return data.get('meta', {}).get('newest_id')

def get_result_count(data):
    """Get result count from meta"""
    return data.get('meta', {}).get('result_count', 0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: x_api_oauth.py tweets <user_id> [since_id]", file=sys.stderr)
        sys.exit(1)
    
    cmd = sys.argv[1]
    user_id = sys.argv[2]
    since_id = sys.argv[3] if len(sys.argv) > 3 else None
    
    if cmd == "tweets":
        result = fetch_tweets_v2(user_id, since_id)
        print(json.dumps(result))
    elif cmd == "tweets_in_window":
        # Args: user_id start_time end_time [since_id]
        if len(sys.argv) < 5:
            print("Usage: x_api_oauth.py tweets_in_window <user_id> <start_time> <end_time> [since_id]", file=sys.stderr)
            sys.exit(1)
        start_time = int(sys.argv[3])
        end_time = int(sys.argv[4])
        since_id = sys.argv[5] if len(sys.argv) > 5 else None
        
        result = fetch_tweets_v2(user_id, since_id)
        if 'error' in result:
            print(json.dumps({"error": result}))
            sys.exit(1)
        
        count = filter_by_window(result, start_time, end_time)
        
        output = {
            "data": result.get('data', []),
            "meta": {
                "result_count": get_result_count(result),
                "newest_id": get_newest_timestamp(result),
                "filtered_count": count
            }
        }
        print(json.dumps(output))
    elif cmd == "token":
        result = get_bearer_token()
        print(json.dumps(result) if isinstance(result, dict) else result)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
