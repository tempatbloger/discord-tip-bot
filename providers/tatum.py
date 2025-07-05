# providers/tatum.py
import requests
from providers.provider_base import CryptoProvider
from config import TATUM_API_KEY
from core.wallet_manager import derive_wallet
from utils.crypto_utils import coin_to_satoshi

HEADERS = {
    "x-api-key": TATUM_API_KEY,
    "Content-Type": "application/json"
}

BASE_URL = "https://api.tatum.io/v3"

SYMBOL_MAP = {
    "BTC": "bitcoin",
    "DOGE": "dogecoin"
}

class Provider(CryptoProvider):
    def get_balance(self, address: str, symbol: str) -> float:
        symbol_l = SYMBOL_MAP[symbol.upper()]
        url = f"{BASE_URL}/{symbol_l}/address/balance/{address}"
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return float(r.json().get("balance", 0))

    def create_transaction(self, from_privkey: str, to_address: str, amount: float, symbol: str) -> str:
        symbol_l = SYMBOL_MAP[symbol.upper()]
        url = f"{BASE_URL}/{symbol_l}/transaction"

        payload = {
            "fromAddress": [
                {
                    "address": derive_wallet("dummy", symbol)["address"],
                    "privateKey": from_privkey
                }
            ],
            "to": [
                {
                    "address": to_address,
                    "value": str(amount)
                }
            ]
        }

        r = requests.post(url, headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json().get("txId")

    def get_deposit_address(self, user_id: str, symbol: str) -> str:
        return derive_wallet(user_id, symbol)["address"]
