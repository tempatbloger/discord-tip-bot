import json
import os
from threading import Lock

USER_DATA_FILE = "data/users.json"
lock = Lock()

# Pastikan direktori data/ ada
os.makedirs("data", exist_ok=True)

# Inisialisasi file user jika belum ada
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

def _load_users():
    with lock:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)

def _save_users(data):
    with lock:
        with open(USER_DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

def get_user_address(user_id: str, symbol: str) -> str:
    data = _load_users()
    return data.get(user_id, {}).get(symbol, {}).get("address")

def get_user_index(user_id: str, symbol: str) -> int:
    data = _load_users()
    return data.get(user_id, {}).get(symbol, {}).get("index", 0)

def set_user_address(user_id: str, symbol: str, address: str, index: int):
    data = _load_users()
    if user_id not in data:
        data[user_id] = {}
    data[user_id][symbol] = {
        "address": address,
        "index": index
    }
    _save_users(data)

def ensure_user_wallet(user_id: str, symbol: str, provider) -> tuple[str, int]:
    """Pastikan user punya address dan index. Jika belum, buatkan."""
    address = get_user_address(user_id, symbol)
    index = get_user_index(user_id, symbol)

    if not address:
        address, index = provider.get_deposit_address(user_id, symbol)
        set_user_address(user_id, symbol, address, index)

    return address, index

def get_user_all_addresses(symbol: str) -> dict[str, str]:
    """
    Mengembalikan dict user_id -> address untuk semua user yang punya address untuk simbol coin tertentu.
    Berguna untuk polling semua address dalam 1 coin (misalnya saat tidak pakai webhook).
    """
    data = _load_users()
    result = {}
    for user_id, coins in data.items():
        if symbol in coins and "address" in coins[symbol]:
            result[user_id] = coins[symbol]["address"]
    return result
