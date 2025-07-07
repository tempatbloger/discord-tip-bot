import discord
import os
from discord.ext import commands
from importlib import import_module
from config import DISCORD_TOKEN, API_PROVIDER

# Setup intents dan bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Simpan provider agar bisa diakses semua command
provider_module = import_module(f"providers.{API_PROVIDER}")
bot.provider = provider_module.Provider()
bot.api_provider = API_PROVIDER  # jika butuh nama modulnya

# Load command dari folder commands/
async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            module = import_module(f"commands.{filename[:-3]}")
            if hasattr(module, "setup"):
                await module.setup(bot)

@bot.event
async def on_ready():
    await load_commands()
    try:
        synced = await bot.tree.sync()
        print(f"? Slash Commands synced globally ({len(synced)} command)")
    except Exception as e:
        print(f"? Gagal sync global commands: {e}")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
