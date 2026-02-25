import time
import requests
from typing import Dict, Any

TOKEN_URL = "https://identity.xero.com/connect/token"
CONNECTIONS_URL = "https://api.xero.com/connections"

def exchange_code_for_tokens(client_id: str, client_secret: str, redirect_uri: str, code: str) -> Dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    r = requests.post(TOKEN_URL, data=data, auth=(client_id, client_secret), timeout=30)
    r.raise_for_status()
    tok = r.json()
    now = int(time.time())
    tok["expires_at"] = now + int(tok["expires_in"])
    return tok

def refresh_tokens(client_id: str, client_secret: str, refresh_token: str) -> Dict[str, Any]:
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    r = requests.post(TOKEN_URL, data=data, auth=(client_id, client_secret), timeout=30)
    r.raise_for_status()
    tok = r.json()
    now = int(time.time())
    tok["expires_at"] = now + int(tok["expires_in"])
    return tok

def fetch_connections(access_token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(CONNECTIONS_URL, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()
