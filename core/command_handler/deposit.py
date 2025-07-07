from core.command_handler.log_utils import _load_log, _save_log

def record_deposit(user_id: str, symbol: str, amount: float) -> None:
    symbol = symbol.upper()
    if amount <= 0:
        return

    log = _load_log()

    for tx in log:
        if (
            tx.get("type") == "deposit"
            and tx["to"] == user_id
            and tx["symbol"] == symbol
            and abs(tx["amount"] - amount) < 1e-8
        ):
            return

    log.append({
        "type": "deposit",
        "from": "onchain",
        "to": user_id,
        "symbol": symbol,
        "amount": amount
    })
    _save_log(log)
