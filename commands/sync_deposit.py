import discord
from config import SUPPORTED_COINS
from core.user_manager import get_user_all_addresses
from core.command_handler import record_deposit


async def setup(bot):
    @bot.tree.command(name="sync_deposit", description="Sinkronisasi deposit on-chain ke saldo internal")
    async def sync_deposit(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("Hanya admin yang bisa menjalankan perintah ini.")
            return

        results = []
        provider = bot.provider

        for symbol in SUPPORTED_COINS:
            address_map = get_user_all_addresses(symbol)
            for user_id, address in address_map.items():
                try:
                    balance = provider.get_balance(address, symbol)
                    if balance > 0:
                        record_deposit(user_id, symbol, balance)
                        results.append(f"? {symbol} {balance:.8f} -> <@{user_id}>")
                except Exception as e:
                    results.append(f"{symbol} {address[:8]}...: {e}")

        if not results:
            await interaction.followup.send("Tidak ada deposit baru ditemukan.")
        else:
            await interaction.followup.send("\n".join(results[:20]))
