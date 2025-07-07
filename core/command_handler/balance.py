from core.command_handler.log_utils import _load_log
from core.user_manager import get_user_address, set_user_address

def get_total_balance(user_id: str, symbol: str, provider) -> float:
    symbol = symbol.upper()
    address = get_user_address(user_id, symbol)
    if not address:
        address, index = provider.get_deposit_address(user_id, symbol)
        set_user_address(user_id, symbol, address, index)

    try:
        onchain_balance = provider.get_balance(address, symbol)
    except:
        onchain_balance = 0.0

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
