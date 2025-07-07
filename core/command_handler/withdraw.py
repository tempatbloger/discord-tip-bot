from core.command_handler.log_utils import _load_log, _save_log
from core.user_manager import get_user_address
from core.wallet_manager import derive_wallet

def withdraw_user(user_id: str, to_address: str, symbol: str, amount: float, provider) -> str:
    symbol = symbol.upper()
    from_address = get_user_address(user_id, symbol)
    if not from_address:
        return "? Kamu belum punya address untuk coin ini."

    try:
        wallet = derive_wallet(user_id, symbol)
        privkey = wallet["private_key"]
        tx_hash = provider.create_transaction(privkey, to_address, amount, symbol)

        log = _load_log()
        log.append({
            "type": "withdraw",
            "from": user_id,
            "to": to_address,
            "symbol": symbol,
            "amount": amount,
            "txid": tx_hash
        })
        _save_log(log)

        return f"? Withdraw {amount:.8f} {symbol} berhasil dikirim.\nTX Hash: `{tx_hash}`"
    except Exception as e:
        return f"? Gagal withdraw: {str(e)}"
