# utils/crypto_utils.py
from decimal import Decimal, ROUND_DOWN

# Konversi satoshi ke koin
def satoshi_to_coin(satoshi: int) -> float:
    return satoshi / 1e8

# Konversi koin ke satoshi
def coin_to_satoshi(amount: float) -> int:
    return int(Decimal(str(amount)).scaleb(8).to_integral_value(rounding=ROUND_DOWN))

# Format angka desimal 8 digit (seperti BTC)
def format_amount(amount: float) -> str:
    return f"{Decimal(amount).quantize(Decimal('0.00000001'))}"
