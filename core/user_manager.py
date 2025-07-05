# core/user_manager.py
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
    return data.get(user_id, {}).get(symbol)

def set_user_address(user_id: str, symbol: str, address: str):
    data = _load_users()
    if user_id not in data:
        data[user_id] = {}
    data[user_id][symbol] = address
    _save_users(data)
