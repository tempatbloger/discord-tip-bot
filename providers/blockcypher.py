import requests
from providers.provider_base import CryptoProvider
from config import BLOCKCYPHER_API_TOKEN

from core.wallet_manager import derive_wallet
from core.user_manager import get_user_index

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
        return data.get("balance", 0) / 1e8  # satoshi ke coin

    def create_transaction(self, from_privkey: str, to_address: str, amount: float, symbol: str) -> str:
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

    def get_deposit_address(self, user_id: str, symbol: str) -> tuple[str, int]:
        """
        Ambil address dari HD wallet berdasarkan user_id dan symbol.
        Jika user belum punya index: buat berdasarkan user_id + symbol hash.
        """
        index = get_user_index(user_id, symbol)
        wallet = derive_wallet(user_id, symbol, index=index)
        return wallet["address"], index
