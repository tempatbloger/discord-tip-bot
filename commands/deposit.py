import discord
from discord import app_commands
from config import SUPPORTED_COINS
from core.user_manager import get_user_address, set_user_address

async def setup(bot):
    @bot.tree.command(name="deposit", description="Dapatkan alamat deposit")
    @app_commands.describe(symbol="Coin (BTC, DOGE, dll)")
    async def deposit(interaction: discord.Interaction, symbol: str):
        await interaction.response.defer(thinking=True)

        symbol = symbol.upper()
        if symbol not in SUPPORTED_COINS:
            await interaction.followup.send(f" Coin {symbol} tidak didukung.")
            return

        user_id = str(interaction.user.id)
        address = get_user_address(user_id, symbol)
        if not address:
            provider = bot.provider
            address, index = provider.get_deposit_address(user_id, symbol)
            set_user_address(user_id, symbol, address, index)

        await interaction.followup.send(f" Alamat deposit {symbol} untuk {interaction.user.mention}:\n`{address}`")
