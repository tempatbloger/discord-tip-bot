# core/wallet_manager.py
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from config import HD_WALLET_SEED

# Fungsi ini menghasilkan private key dan address deterministik berbasis user_id

def derive_wallet(user_id: str, symbol: str, index: int = 0) -> dict:
    from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
    from config import HD_WALLET_SEED

    # Buat seed dari mnemonic
    seed_bytes = Bip39SeedGenerator(HD_WALLET_SEED).Generate()

    # Pilih coin path
    coin_map = {
        "BTC": Bip44Coins.BITCOIN,
        "DOGE": Bip44Coins.DOGECOIN,
        # Tambahkan coin lain sesuai kebutuhan
    }

    if symbol not in coin_map:
        raise ValueError(f"Coin {symbol} tidak didukung untuk HD Wallet")

    bip44_def_ctx = Bip44.FromSeed(seed_bytes, coin_map[symbol])
    bip44_acc_ctx = bip44_def_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(index)

    return {
        "address": bip44_addr_ctx.PublicKey().ToAddress(),
        "private_key": bip44_addr_ctx.PrivateKey().ToWif(),
        "index": index
    }
