import os
import json
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

from core.command_handler import tip_user, get_total_balance
from config import SUPPORTED_COINS
from config import API_PROVIDER
from importlib import import_module

provider_module = import_module(f"providers.{API_PROVIDER}")
provider = provider_module.Provider()

CLAIM_FILE = "data/faucet_claims.json"

# Jumlah faucet per coin (bisa kamu ubah sesuai kebutuhan)
FAUCET_AMOUNT = {
    "DOGE":0.0001,
    "BTC": 0.00000001,
}

# Helper untuk klaim log
def load_claims():
    if not os.path.exists(CLAIM_FILE):
        return {}
    with open(CLAIM_FILE, "r") as f:
        return json.load(f)

def save_claims(data):
    with open(CLAIM_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def setup(bot: commands.Bot):
    @bot.tree.command(name="faucet", description="Klaim koin gratis dari faucet (1x/24 jam)")
    @app_commands.describe(symbol="Coin yang ingin kamu klaim (DOGE, BTC, dll)")
    async def faucet(interaction: discord.Interaction, symbol: str):
        await interaction.response.defer(thinking=True)

        symbol = symbol.upper()
        user_id = str(interaction.user.id)

        if symbol not in SUPPORTED_COINS:
            await interaction.followup.send(f" Coin {symbol} tidak tersedia.")
            return

        now = datetime.utcnow()
        claims = load_claims()
        last_claim_str = claims.get(user_id, {}).get(symbol)

        if last_claim_str:
            last_claim_time = datetime.fromisoformat(last_claim_str)
            if now - last_claim_time < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last_claim_time)
                hours, remainder = divmod(remaining.total_seconds(), 3600)
                minutes = remainder // 60
                await interaction.followup.send(
                    f"Kamu sudah klaim {symbol} hari ini.\n"
                    f"Coba lagi dalam {int(hours)} jam {int(minutes)} menit."
                )
                return

        amount = FAUCET_AMOUNT.get(symbol, 0.0)
        if amount <= 0:
            await interaction.followup.send(f" Faucet untuk {symbol} belum diaktifkan.")
            return

        # Cek saldo FAUCET
        faucet_balance = get_total_balance("FAUCET", symbol, provider)
        if faucet_balance < amount:
            await interaction.followup.send(
                f"?? Faucet kehabisan {symbol}.\n"
                f"Silakan donasi dengan command: `/tip @GoTipBot {symbol} <jumlah>`"
            )
            return

        # Transfer dari FAUCET ke user
        result = tip_user("FAUCET", user_id, symbol, amount)

        # Update waktu klaim
        claims.setdefault(user_id, {})[symbol] = now.isoformat()
        save_claims(claims)

        await interaction.followup.send(
            f"Kamu berhasil klaim {amount:.8f} {symbol} dari faucet!\n{result}"
        )
