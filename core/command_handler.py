# core/command_handler.py
import json
import os
from threading import Lock

from core.user_manager import get_user_address
from core.wallet_manager import derive_wallet
from config import SUPPORTED_COINS

TIP_LOG_FILE = "data/transactions.log"
lock = Lock()

# Buat file transaksi jika belum ada
os.makedirs("data", exist_ok=True)
if not os.path.exists(TIP_LOG_FILE):
    with open(TIP_LOG_FILE, "w") as f:
        json.dump([], f)

def _load_log():
    with lock:
        with open(TIP_LOG_FILE, "r") as f:
            return json.load(f)

def _save_log(data):
    with lock:
        with open(TIP_LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

def tip_user(sender_id: str, receiver_id: str, symbol: str, amount: float) -> str:
    if symbol not in SUPPORTED_COINS:
        return "? Coin tidak didukung."

    if sender_id == receiver_id:
        return "?? Tidak bisa tip ke diri sendiri."

    tx = {
        "from": sender_id,
        "to": receiver_id,
        "symbol": symbol,
        "amount": amount
    }

    log = _load_log()
    log.append(tx)
    _save_log(log)

    return f"? {amount:.8f} {symbol} telah dikirim dari <@{sender_id}> ke <@{receiver_id}>."

def withdraw_user(user_id: str, to_address: str, symbol: str, amount: float, provider) -> str:
    from_address = get_user_address(user_id, symbol)
    if not from_address:
        return "? Kamu belum punya address untuk coin ini."

    try:
        wallet = derive_wallet(user_id, symbol)
        privkey = wallet["private_key"]
        tx_hash = provider.create_transaction(privkey, to_address, amount, symbol)
        return f"?? Withdraw {amount:.8f} {symbol} berhasil dikirim. TX Hash: `{tx_hash}`"
    except Exception as e:
        return f"? Gagal withdraw: {str(e)}"
