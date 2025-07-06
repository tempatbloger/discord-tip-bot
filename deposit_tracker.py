import time
from providers.dogecoin_node import Provider
from core.user_manager import get_user_all_addresses
from core.command_handler import record_deposit

# Inisialisasi provider sesuai dengan yang digunakan
provider = Provider()
SYMBOL = "DOGE"
POLL_INTERVAL = 60  # detik

print(f"[??] Deposit tracker aktif untuk {SYMBOL} setiap {POLL_INTERVAL} detik...")

while True:
    print("[?] Memulai polling deposit...")
    user_addresses = get_user_all_addresses(SYMBOL)

    for user_id, address in user_addresses.items():
        try:
            txs = provider.list_transactions(address, SYMBOL)
            for tx in txs:
                if tx["confirmations"] >= 1 and tx["amount"] > 0:
                    record_deposit(user_id, SYMBOL, tx["amount"])
                    print(f"[?] Deposit: {tx['amount']} {SYMBOL} untuk user {user_id}")
        except Exception as e:
            print(f"[??] Gagal memeriksa address {address}: {e}")

    time.sleep(POLL_INTERVAL)
