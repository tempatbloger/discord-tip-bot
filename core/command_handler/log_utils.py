import os
import json
from threading import Lock

TIP_LOG_FILE = "data/transactions.log"
lock = Lock()

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

def append_log_entry(entry: dict):
    """Tambahkan 1 transaksi ke log"""
    data = _load_log()
    data.append(entry)
    _save_log(data)
