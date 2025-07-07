import discord
from discord import app_commands
from config import SUPPORTED_COINS
from core.command_handler import get_total_balance

async def setup(bot):
    @bot.tree.command(name="balance", description="Cek semua saldo kamu")
    async def balance(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        user_id = str(interaction.user.id)
        username = interaction.user.name
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None

        coin_emojis = {
    "BTC": "",
    "DOGE": "",
    "ETH": "",
    "LTC": "",
    "SOL": "",
    "ADA": ""
	}
        embed = discord.Embed(
            title="Total Saldo",
            description="Berikut saldo kamu untuk semua coin:",
            color=0x2ecc71
        )

        from importlib import import_module
        provider = import_module(f"providers.{bot.api_provider}").Provider()

        for symbol in SUPPORTED_COINS:
            try:
                balance = get_total_balance(user_id, symbol, provider)
                emoji = coin_emojis.get(symbol, "")
                embed.add_field(
                    name=f"{emoji} {symbol}",
                    value=f"{balance:.8f} {symbol}",
                    inline=True
                )
            except Exception as e:
                embed.add_field(name=f"{symbol}", value=f"Gagal: {e}", inline=True)

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)
            embed.set_author(name=username, icon_url=avatar_url)

        embed.set_footer(text="Gunakan /deposit untuk melihat alamat wallet kamu.")
        await interaction.followup.send(embed=embed)
