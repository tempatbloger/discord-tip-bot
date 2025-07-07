import discord
from discord.ext import commands
from discord import app_commands

from config import SUPPORTED_COINS
from core.command_handler import get_total_balance

# Tambahkan provider
from importlib import import_module
from config import API_PROVIDER

provider_module = import_module(f"providers.{API_PROVIDER}")
provider = provider_module.Provider()

async def setup(bot: commands.Bot):
    @bot.tree.command(name="faucet_balance", description="Lihat saldo faucet untuk semua coin")
    async def faucet_balance(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        embed = discord.Embed(
            title=" Saldo Faucet",
            description="Saldo akun faucet saat ini untuk tiap coin:",
            color=0x3498db
        )

        has_balance = False

        for symbol in SUPPORTED_COINS:
            try:
                balance = get_total_balance("FAUCET", symbol, provider)
                if balance > 0:
                    has_balance = True
                    embed.add_field(name=symbol, value=f"{balance:.8f} {symbol}", inline=True)
            except Exception as e:
                embed.add_field(name=symbol, value=f"Error: {e}", inline=True)

        if not has_balance:
            embed.description += "\n\n Faucet kosong. Silakan donasi dengan `/tip @GoTipBot <coin> <jumlah>`."

        await interaction.followup.send(embed=embed)
