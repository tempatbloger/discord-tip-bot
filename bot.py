# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands
from importlib import import_module
from config import DISCORD_TOKEN, API_PROVIDER, SUPPORTED_COINS
from core.user_manager import get_user_address, set_user_address
from core.command_handler import tip_user, withdraw_user, get_total_balance

# Load API provider
provider_module = import_module(f"providers.{API_PROVIDER}")
provider = provider_module.Provider()

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# ========== EVENTS ==========

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    try:
        synced = await bot.tree.sync()  # GLOBAL SYNC
        print(f"? Slash Commands synced globally ({len(synced)} command)")
    except Exception as e:
        print(f"? Gagal sync global commands: {e}")

# ========== COMMAND: BALANCE ==========

@bot.tree.command(name="balance", description="Cek semua saldo kamu")
async def balance(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    user_id = str(interaction.user.id)
    username = interaction.user.name
    avatar_url = interaction.user.avatar.url if interaction.user.avatar else None

    coin_emojis = {
        "BTC": "?",
        "DOGE": "?",
        "ETH": "?",
        "LTC": "?",
        "SOL": "?",
        "ADA": "?",
    }

    embed = discord.Embed(
        title="?? Total Saldo",
        description="Berikut saldo kamu untuk semua coin:",
        color=0x2ecc71
    )

    for symbol in SUPPORTED_COINS:
        try:
            balance = get_total_balance(user_id, symbol, provider)
            emoji = coin_emojis.get(symbol, "??")
            embed.add_field(
                name=f"{emoji} {symbol}",
                value=f"{balance:.8f} {symbol}",
                inline=True
            )
        except Exception as e:
            embed.add_field(
                name=f"{symbol}",
                value=f"Gagal: {e}",
                inline=True
            )

    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name=username, icon_url=avatar_url)

    embed.set_footer(text="Gunakan /deposit untuk melihat alamat wallet kamu.")
    await interaction.followup.send(embed=embed)

# ========== COMMAND: DEPOSIT ==========

@bot.tree.command(name="deposit", description="Dapatkan alamat deposit")
@app_commands.describe(symbol="Coin (BTC, DOGE, dll)")
async def deposit(interaction: discord.Interaction, symbol: str):
    await interaction.response.defer(thinking=True)

    symbol = symbol.upper()
    if symbol not in SUPPORTED_COINS:
        await interaction.followup.send(f"?? Coin {symbol} tidak didukung.")
        return

    user_id = str(interaction.user.id)
    address = get_user_address(user_id, symbol)
    if not address:
        address, index = provider.get_deposit_address(user_id, symbol)
        set_user_address(user_id, symbol, address, index)

    await interaction.followup.send(f"?? Alamat deposit {symbol} untuk {interaction.user.mention}:\n`{address}`")

# ========== COMMAND: TIP ==========

@bot.tree.command(name="tip", description="Kirim coin ke user lain (internal)")
@app_commands.describe(member="User tujuan", symbol="Coin", amount="Jumlah")
async def tip(interaction: discord.Interaction, member: discord.Member, symbol: str, amount: float):
    await interaction.response.defer(thinking=True)

    symbol = symbol.upper()
    sender_id = str(interaction.user.id)
    receiver_id = str(member.id)

    result = tip_user(sender_id, receiver_id, symbol, amount)
    await interaction.followup.send(result)

# ========== COMMAND: WITHDRAW ==========

@bot.tree.command(name="withdraw", description="Tarik coin ke wallet")
@app_commands.describe(symbol="Coin", to_address="Alamat tujuan", amount="Jumlah")
async def withdraw(interaction: discord.Interaction, symbol: str, to_address: str, amount: float):
    await interaction.response.defer(thinking=True)

    symbol = symbol.upper()
    user_id = str(interaction.user.id)

    result = withdraw_user(user_id, to_address, symbol, amount, provider)
    await interaction.followup.send(result)
# ========== COMMAND: SYNC_DEPOSIT ==========

@bot.tree.command(name="sync_deposit", description="?? Sinkronisasi deposit on-chain ke saldo internal")
async def sync_deposit(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("? Hanya admin yang bisa menjalankan perintah ini.")
        return

    results = []
    for symbol in SUPPORTED_COINS:
        address_map = get_user_all_addresses(symbol)
        for user_id, address in address_map.items():
            try:
                balance = provider.get_balance(address, symbol)
                if balance > 0:
                    record_deposit(user_id, symbol, balance)
                    results.append(f"? {symbol} {balance:.8f} -> <@{user_id}>")
            except Exception as e:
                results.append(f"? {symbol} {address[:8]}...: {e}")

    if not results:
        await interaction.followup.send("?? Tidak ada deposit baru ditemukan.")
    else:
        await interaction.followup.send("\n".join(results[:20]))  # batasi 20 baris pertama

# ========== START BOT ==========

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
