# providers/nownodes.py
import requests
from providers.provider_base import CryptoProvider
from config import NOWNODES_API_KEY

HEADERS = {
    "api-key": NOWNODES_API_KEY
}

BASE_URLS = {
    "BTC": "https://btcbook.nownodes.io/api/v2",
    "DOGE": "https://dogebook.nownodes.io/api/v2"
}

class Provider(CryptoProvider):
    def get_balance(self, address: str, symbol: str) -> float:
        url = f"{BASE_URLS[symbol]}/address/{address}"
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        return data.get("balance", 0) / 1e8

    def create_transaction(self, from_privkey: str, to_address: str, amount: float, symbol: str) -> str:
        raise NotImplementedError("? NowNodes tidak menyediakan TX builder langsung.")

    def get_deposit_address(self, user_id: str, symbol: str) -> str:
        # Dalam implementasi nyata, gunakan wallet manager
        from core.wallet_manager import derive_wallet
        return derive_wallet(user_id, symbol)["address"]
