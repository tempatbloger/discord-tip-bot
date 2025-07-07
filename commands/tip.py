import discord
from discord import app_commands
from core.command_handler import tip_user

async def setup(bot):
    @bot.tree.command(name="tip", description="Kirim coin ke user lain (internal)")
    @app_commands.describe(member="User tujuan", symbol="Coin", amount="Jumlah")
    async def tip(interaction: discord.Interaction, member: discord.Member, symbol: str, amount: float):
        await interaction.response.defer(thinking=True)

        symbol = symbol.upper()
        sender_id = str(interaction.user.id)
        receiver_id = str(member.id)

        result = tip_user(sender_id, receiver_id, symbol, amount)
        await interaction.followup.send(result)
