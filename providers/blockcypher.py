# providers/blockcypher.py
import requests
from providers.provider_base import CryptoProvider
from config import BLOCKCYPHER_API_TOKEN

BASE_URLS = {
    "BTC": "https://api.blockcypher.com/v1/btc/main",
    "DOGE": "https://api.blockcypher.com/v1/doge/main"
}

class Provider(CryptoProvider):
    def get_balance(self, address: str, symbol: str) -> float:
        url = f"{BASE_URLS[symbol]}/addrs/{address}/balance"
        params = {"token": BLOCKCYPHER_API_TOKEN}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        return data.get("balance", 0) / 1e8  # convert satoshi to coin unit

    def create_transaction(self, from_privkey: str, to_address: str, amount: float, symbol: str) -> str:
        # NOTE: For simplicity, this uses BlockCypher's built-in TX API
        url = f"{BASE_URLS[symbol]}/txs/micro"
        payload = {
            "from_private": from_privkey,
            "to_address": to_address,
            "value_satoshis": int(amount * 1e8),
            "token": BLOCKCYPHER_API_TOKEN
        }
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json().get("tx", {}).get("hash")

    def get_deposit_address(self, user_id: str, symbol: str) -> str:
        # Ideally: return user wallet (generated elsewhere)
        # For demo: create new address each time (not safe for production)
        url = f"{BASE_URLS[symbol]}/addrs"
        params = {"token": BLOCKCYPHER_API_TOKEN}
        r = requests.post(url, params=params)
        r.raise_for_status()
        return r.json().get("address")
