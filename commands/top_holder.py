import discord
from discord.ext import commands
from discord import app_commands
from config import SUPPORTED_COINS, API_PROVIDER
from core.command_handler import get_total_balance
from core.user_manager import get_all_user_ids
from importlib import import_module

provider_module = import_module(f"providers.{API_PROVIDER}")
provider = provider_module.Provider()

COIN_EMOJIS = {
    "DOGE": "",
    "BTC": "",
    "ETH": "",
    "LTC": ""
}

async def setup(bot: commands.Bot):
    @bot.tree.command(name="top_holder", description=" Lihat 10 pengguna dengan saldo coin terbanyak")
    @app_commands.describe(symbol="Coin (DOGE, BTC, dll)")
    async def top_holder(interaction: discord.Interaction, symbol: str):
        await interaction.response.defer(thinking=True)

        symbol = symbol.upper()
        if symbol not in SUPPORTED_COINS:
            await interaction.followup.send(f" Coin {symbol} tidak tersedia.")
            return

        try:
            user_ids = [uid for uid in get_all_user_ids() if uid != "FAUCET"]
        except Exception as e:
            await interaction.followup.send(f" Gagal mengambil daftar user: {e}")
            return

        balances = []
        for user_id in user_ids:
            try:
                total = get_total_balance(user_id, symbol, provider)
                if total > 0:
                    balances.append((user_id, total))
            except:
                continue  # abaikan error user

        if not balances:
            await interaction.followup.send(f" Belum ada saldo {symbol} di sistem.")
            return

        top = sorted(balances, key=lambda x: x[1], reverse=True)[:10]
        emoji = COIN_EMOJIS.get(symbol, "??")

        embed = discord.Embed(
            title=f"{emoji} Top Holder {symbol}",
            description=f"10 pengguna dengan total saldo {symbol} terbanyak (on-chain + internal)",
            color=0x1abc9c
        )

        for i, (user_id, amount) in enumerate(top, start=1):
            embed.add_field(
                name=f"{i}. <@{user_id}>",
                value=f"{amount:.8f} {symbol}",
                inline=False
            )

        await interaction.followup.send(embed=embed)
