# core/wallet_manager.py
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from config import HD_WALLET_SEED

# Fungsi ini menghasilkan private key dan address deterministik berbasis user_id

def derive_wallet(user_id: str, symbol: str):
    symbol = symbol.upper()
    
    # Peta simbol koin ke BIP44 coin
    coin_map = {
        "BTC": Bip44Coins.BITCOIN,
        "DOGE": Bip44Coins.DOGECOIN
    }
    
    if symbol not in coin_map:
        raise ValueError("Coin tidak didukung oleh wallet_manager.")

    # Gunakan user_id sebagai indeks derivasi agar unik
    index = int(user_id) % 2**31  # pastikan tidak overflow

    # Generate seed dan derive
    seed_bytes = Bip39SeedGenerator(HD_WALLET_SEED).Generate()
    bip_obj = Bip44.FromSeed(seed_bytes, coin_map[symbol])
    acct = bip_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)

    return {
        "address": acct.PublicKey().ToAddress(),
        "private_key": acct.PrivateKey().Raw().ToHex()
    }

# Contoh pakai:
# wallet = derive_wallet("123456789", "BTC")
# print(wallet["address"], wallet["private_key"])
