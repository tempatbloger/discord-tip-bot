import requests
from decimal import Decimal
from providers.provider_base import CryptoProvider
from core.wallet_manager import derive_wallet
from core.user_manager import get_user_index
from bitcoinlib.keys import HDKey


class DogecoinRPC:
    def __init__(self, user: str, password: str, host: str = "127.0.0.1", port: int = 22555):
        self.url = f"http://{user}:{password}@{host}:{port}"

    def call(self, method: str, params: list = []):
        payload = {
            "jsonrpc": "1.0",
            "id": "tipbot",
            "method": method,
            "params": params
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            raise Exception(f"RPC Error: {data['error']}")
        return data["result"]


class Provider(CryptoProvider):
    def __init__(self):
        from config import DOGE_RPC_USER, DOGE_RPC_PASS, DOGE_RPC_HOST, DOGE_RPC_PORT
        self.rpc = DogecoinRPC(DOGE_RPC_USER, DOGE_RPC_PASS, DOGE_RPC_HOST, DOGE_RPC_PORT)

    def get_balance(self, address: str, symbol: str) -> float:
        try:
            balance = self.rpc.call("getreceivedbyaddress", [address, 0])
            return float(balance)
        except Exception as e:
            print(f"[RPC] Gagal ambil saldo: {e}")
            return 0.0

    def create_transaction(self, from_privkey: str, to_address: str, amount: float, symbol: str) -> str:
        key = HDKey(import_key=from_privkey, network='dogecoin')
        from_address = key.address()

        # Ambil UTXO dari address
        utxos = self.rpc.call("listunspent", [1, 9999999, [from_address]])
        if not utxos:
            raise Exception("UTXO kosong. Tidak ada saldo untuk ditransaksikan.")

        total_input = Decimal('0')
        inputs = []
        for utxo in utxos:
            inputs.append({
                "txid": utxo["txid"],
                "vout": utxo["vout"]
            })
            total_input += Decimal(str(utxo["amount"]))
            if total_input >= Decimal(str(amount)) + Decimal("1"):
                break

        if total_input < Decimal(str(amount)):
            raise Exception("Saldo tidak cukup untuk transaksi.")

        fee = Decimal("0.5")
        change = total_input - Decimal(str(amount)) - fee

        outputs = {
            to_address: float(amount)
        }
        if change > 0:
            outputs[from_address] = float(change)

        # Buat raw transaction
        raw_tx = self.rpc.call("createrawtransaction", [inputs, outputs])

        # Sign dengan private key
        signed = self.rpc.call("signrawtransactionwithkey", [raw_tx, [from_privkey]])
        if not signed.get("complete"):
            raise Exception("Gagal sign transaksi.")

        # Broadcast
        txid = self.rpc.call("sendrawtransaction", [signed["hex"]])
        return txid

    def get_deposit_address(self, user_id: str, symbol: str) -> tuple[str, int]:
        index = get_user_index(user_id, symbol)
        wallet = derive_wallet(user_id, symbol, index=index)
        address = wallet["address"]

        try:
            self.rpc.call("importaddress", [address, "", False])
        except Exception as e:
            print(f"[RPC] importaddress error: {e}")

        return address, index

    def list_transactions(self, address: str, symbol: str) -> list[dict]:
        """
        Mengambil semua transaksi masuk (received) untuk address tertentu.
        Digunakan untuk mendeteksi deposit on-chain ke address user.
        """
        try:
            tx_list = self.rpc.call("listtransactions", ["*", 100, 0, True])  # 100 transaksi terakhir
            result = []
            for tx in tx_list:
                if tx.get("category") == "receive" and tx.get("address") == address:
                    result.append({
                        "txid": tx["txid"],
                        "amount": float(tx["amount"]),
                        "confirmations": tx["confirmations"],
                        "time": tx["time"]
                    })
            return result
        except Exception as e:
            print(f"[RPC] Gagal ambil transaksi address {address}: {e}")
            return []
