import json
import os
from threading import Lock

from core.user_manager import get_user_address, set_user_address
from core.wallet_manager import derive_wallet
from config import SUPPORTED_COINS

TIP_LOG_FILE = "data/transactions.log"
lock = Lock()

# Pastikan folder data dan file log ada
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
    symbol = symbol.upper()

    if symbol not in SUPPORTED_COINS:
        return "? Coin tidak didukung."

    if sender_id == receiver_id:
        return "? Tidak bisa tip ke diri sendiri."

    if amount <= 0:
        return "? Jumlah harus lebih dari 0."

    log = _load_log()
    balances = {}

    for tx in log:
        coin = tx["symbol"]
        balances.setdefault(coin, {})
        balances[coin].setdefault(tx["from"], 0)
        balances[coin].setdefault(tx["to"], 0)
        balances[coin][tx["from"]] -= tx["amount"]
        balances[coin][tx["to"]] += tx["amount"]

    sender_balance = balances.get(symbol, {}).get(sender_id, 0)

    if sender_balance < amount:
        return f"? Gagal: saldo {symbol} kamu hanya {sender_balance:.8f}, tidak cukup untuk tip {amount:.8f}."

    tx = {
        "type": "tip",
        "from": sender_id,
        "to": receiver_id,
        "symbol": symbol,
        "amount": amount
    }

    log.append(tx)
    _save_log(log)

    return f"? {amount:.8f} {symbol} telah dikirim dari <@{sender_id}> ke <@{receiver_id}>."

def withdraw_user(user_id: str, to_address: str, symbol: str, amount: float, provider) -> str:
    symbol = symbol.upper()
    from_address = get_user_address(user_id, symbol)
    if not from_address:
        return "? Kamu belum punya address untuk coin ini."

    try:
        wallet = derive_wallet(user_id, symbol)
        privkey = wallet["private_key"]
        tx_hash = provider.create_transaction(privkey, to_address, amount, symbol)

        # Tambahkan log withdraw
        log = _load_log()
        tx = {
            "type": "withdraw",
            "from": user_id,
            "to": to_address,
            "symbol": symbol,
            "amount": amount,
            "txid": tx_hash
        }
        log.append(tx)
        _save_log(log)

        return f"? Withdraw {amount:.8f} {symbol} berhasil dikirim.\nTX Hash: `{tx_hash}`"
    except Exception as e:
        return f"? Gagal withdraw: {str(e)}"

def get_total_balance(user_id: str, symbol: str, provider) -> float:
    symbol = symbol.upper()
    address = get_user_address(user_id, symbol)

    # Jika belum ada, buat address + index dan simpan
    if not address:
        address, index = provider.get_deposit_address(user_id, symbol)
        set_user_address(user_id, symbol, address, index)

    try:
        onchain_balance = provider.get_balance(address, symbol)
    except:
        onchain_balance = 0.0

    # Hitung saldo internal dari log tip dan deposit
    log = _load_log()
    internal_total = 0.0
    for tx in log:
        if tx["symbol"] != symbol:
            continue
        if tx["from"] == user_id:
            internal_total -= tx["amount"]
        if tx["to"] == user_id:
            internal_total += tx["amount"]

    return round(onchain_balance + internal_total, 8)

def record_deposit(user_id: str, symbol: str, amount: float) -> None:
    """
    Mencatat transaksi deposit dari on-chain ke log internal (sekali saja).
    Dipanggil saat webhook atau polling mendeteksi transaksi masuk.
    """
    symbol = symbol.upper()
    if amount <= 0:
        return  # Abaikan deposit 0 atau negatif

    log = _load_log()

    # Cek apakah sudah pernah dicatat sebelumnya
    for tx in log:
        if (
            tx.get("type") == "deposit"
            and tx["to"] == user_id
            and tx["symbol"] == symbol
            and abs(tx["amount"] - amount) < 1e-8
        ):
            return  # Sudah tercatat, abaikan

    tx = {
        "type": "deposit",
        "from": "onchain",
        "to": user_id,
        "symbol": symbol,
        "amount": amount
    }

    log.append(tx)
    _save_log(log)
