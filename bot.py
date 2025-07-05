# bot.py
import discord
from discord.ext import commands
from importlib import import_module

from config import DISCORD_TOKEN, API_PROVIDER, SUPPORTED_COINS
from core.user_manager import get_user_address, set_user_address
from core.command_handler import tip_user, withdraw_user

# Load API provider secara dinamis
provider_module = import_module(f"providers.{API_PROVIDER}")
provider = provider_module.Provider()

# Prefix slash command
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# ===================== COMMANDS =====================

@bot.command()
async def balance(ctx, symbol: str):
    symbol = symbol.upper()
    if symbol not in SUPPORTED_COINS:
        await ctx.send(f"? Coin {symbol} tidak didukung.")
        return

    user_id = str(ctx.author.id)
    address = get_user_address(user_id, symbol)
    if not address:
        address = provider.get_deposit_address(user_id, symbol)
        set_user_address(user_id, symbol, address)

    bal = provider.get_balance(address, symbol)
    await ctx.send(f"?? Balance {symbol} untuk {ctx.author.mention}: {bal:.8f} {symbol}")


@bot.command()
async def deposit(ctx, symbol: str):
    symbol = symbol.upper()
    if symbol not in SUPPORTED_COINS:
        await ctx.send(f"? Coin {symbol} tidak didukung.")
        return

    user_id = str(ctx.author.id)
    address = get_user_address(user_id, symbol)
    if not address:
        address = provider.get_deposit_address(user_id, symbol)
        set_user_address(user_id, symbol, address)

    await ctx.send(f"?? Deposit address {symbol} untuk {ctx.author.mention}: `{address}`")


@bot.command()
async def tip(ctx, member: discord.Member, symbol: str, amount: float):
    symbol = symbol.upper()
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)
    
    result = tip_user(sender_id, receiver_id, symbol, amount)
    await ctx.send(result)


@bot.command()
async def withdraw(ctx, symbol: str, to_address: str, amount: float):
    symbol = symbol.upper()
    user_id = str(ctx.author.id)

    result = withdraw_user(user_id, to_address, symbol, amount, provider)
    await ctx.send(result)


# Start bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
