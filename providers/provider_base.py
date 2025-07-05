# providers/provider_base.py
from abc import ABC, abstractmethod

class CryptoProvider(ABC):
    @abstractmethod
    def get_balance(self, address: str, symbol: str) -> float:
        pass

    @abstractmethod
    def create_transaction(self, from_privkey: str, to_address: str, amount: float, symbol: str) -> str:
        pass

    @abstractmethod
    def get_deposit_address(self, user_id: str, symbol: str) -> str:
        pass
