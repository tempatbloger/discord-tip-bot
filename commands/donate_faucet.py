import discord
from discord import app_commands
from discord.ext import commands

from config import SUPPORTED_COINS
from core.command_handler import tip_user

async def setup(bot: commands.Bot):
    @bot.tree.command(name="donate_faucet", description="Donasi koin ke faucet agar bisa dibagikan ke user lain")
    @app_commands.describe(symbol="Koin yang ingin didonasikan (DOGE, BTC, dll)", amount="Jumlah koin")
    async def donate_faucet(interaction: discord.Interaction, symbol: str, amount: float):
        await interaction.response.defer(thinking=True)

        user_id = str(interaction.user.id)
        symbol = symbol.upper()

        if symbol not in SUPPORTED_COINS:
            await interaction.followup.send(f" Coin {symbol} tidak tersedia.")
            return

        if amount <= 0:
            await interaction.followup.send(f" Jumlah harus lebih dari 0.")
            return

        result = tip_user(user_id, "@GoTipBot", symbol, amount)

        await interaction.followup.send(
            f" Terima kasih telah berdonasi ke faucet!\n{result}\n\n"
            f"Kamu bisa cek saldo faucet dengan command `/faucet_balance`."
        )
