from core.command_handler.log_utils import _load_log, _save_log
from config import SUPPORTED_COINS

def tip_user(sender_id: str, receiver_id: str, symbol: str, amount: float) -> str:
    symbol = symbol.upper()

    if symbol not in SUPPORTED_COINS:
        return "?? Coin tidak didukung."
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
        return f"? Saldo {symbol} kamu hanya {sender_balance:.8f}, tidak cukup untuk tip {amount:.8f}."

    log.append({
        "type": "tip",
        "from": sender_id,
        "to": receiver_id,
        "symbol": symbol,
        "amount": amount
    })
    _save_log(log)

    return f"?? {amount:.8f} {symbol} telah dikirim dari <@{sender_id}> ke <@{receiver_id}>."
