import discord
from discord import app_commands
from core.command_handler import withdraw_user

async def setup(bot):
    @bot.tree.command(name="withdraw", description="Tarik coin ke wallet")
    @app_commands.describe(symbol="Coin", to_address="Alamat tujuan", amount="Jumlah")
    async def withdraw(interaction: discord.Interaction, symbol: str, to_address: str, amount: float):
        await interaction.response.defer(thinking=True)

        symbol = symbol.upper()
        user_id = str(interaction.user.id)
        result = withdraw_user(user_id, to_address, symbol, amount, bot.provider)
        await interaction.followup.send(result)
