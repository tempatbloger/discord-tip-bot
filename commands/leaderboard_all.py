import os
import json
import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict, Counter

from config import SUPPORTED_COINS

TIP_LOG_FILE = "data/transactions.log"

async def setup(bot: commands.Bot):
    @bot.tree.command(name="leaderboard_all", description=" Lihat leaderboard tip & donasi (3 kategori)")
    @app_commands.describe(symbol="Coin untuk leaderboard (DOGE, BTC, dll)")
    async def leaderboard_all(interaction: discord.Interaction, symbol: str):
        await interaction.response.defer(thinking=True)

        symbol = symbol.upper()
        if symbol not in SUPPORTED_COINS:
            await interaction.followup.send(f" Coin {symbol} tidak tersedia.")
            return

        if not os.path.exists(TIP_LOG_FILE):
            await interaction.followup.send(" Belum ada transaksi yang tercatat.")
            return

        with open(TIP_LOG_FILE, "r") as f:
            try:
                txs = json.load(f)
            except:
                await interaction.followup.send(" Gagal membaca file transaksi.")
                return

        # 1. Total tip diterima
        tips_received = defaultdict(float)
        for tx in txs:
            if tx.get("type") == "tip" and tx.get("symbol") == symbol:
                tips_received[tx["to"]] += tx["amount"]

        # 2. Total donasi ke faucet
        donate_amounts = defaultdict(float)
        # 3. Jumlah donasi ke faucet (frekuensi)
        donate_counts = Counter()
        for tx in txs:
            if tx.get("type") == "tip" and tx.get("symbol") == symbol and tx.get("to") == "FAUCET":
                donate_amounts[tx["from"]] += tx["amount"]
                donate_counts[tx["from"]] += 1

        embed = discord.Embed(
            title=f"Leaderboard Gabungan - {symbol}",
            description="Berikut 3 leaderboard teratas untuk aktivitas tip & donasi:",
            color=0x8e44ad
        )

        # --- TIPS DITERIMA ---
        embed.add_field(name="Tip Terbanyak Diterima", value=" ", inline=False)
        for i, (uid, amt) in enumerate(sorted(tips_received.items(), key=lambda x: x[1], reverse=True)[:10], 1):
            embed.add_field(name=f"{i}. <@{uid}>", value=f"{amt:.8f} {symbol}", inline=True)

        # --- DONASI TERBANYAK (JUMLAH) ---
        embed.add_field(name="Donasi Terbanyak (Jumlah)", value=" ", inline=False)
        for i, (uid, amt) in enumerate(sorted(donate_amounts.items(), key=lambda x: x[1], reverse=True)[:10], 1):
            embed.add_field(name=f"{i}. <@{uid}>", value=f"{amt:.8f} {symbol}", inline=True)

        # --- DONASI TERBANYAK (FREKUENSI) ---
        embed.add_field(name="Donasi Terbanyak (Jumlah Transaksi)", value=" ", inline=False)
        for i, (uid, count) in enumerate(donate_counts.most_common(10), 1):
            embed.add_field(name=f"{i}. <@{uid}>", value=f"{count} donasi", inline=True)

        await interaction.followup.send(embed=embed)
