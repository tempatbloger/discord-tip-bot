# 🚀 GoTipBot — Discord Crypto Tip Bot

**GoTipBot** adalah bot Discord yang memungkinkan pengguna saling mengirim, menerima, menyimpan, menarik, dan menyumbangkan cryptocurrency secara mudah di dalam server Discord.

---

## 📦 Fitur Utama

| Command               | Fungsi                                                                 |
|-----------------------|------------------------------------------------------------------------|
| `/balance`            | Cek saldo semua koin kamu                                              |
| `/deposit`            | Lihat alamat deposit kamu untuk tiap koin                              |
| `/tip`                | Kirim koin ke user lain dalam server                                   |
| `/withdraw`           | Tarik koin ke alamat wallet eksternal                                  |
| `/sync_deposit`       | (Admin) Sinkronisasi deposit dari on-chain ke internal balance         |
| `/faucet`             | Klaim saldo gratis dari saldo bot (1x per user per periode)            |
| `/faucet_balance`     | Lihat saldo Faucet saat ini                                            |
| `/top_holder`         | Lihat 10 user dengan saldo terbesar untuk 1 koin                       |


---

## 📁 Struktur Proyek
├── bot.py # Entry point utama bot
├── commands/ # Folder semua command modular
│ ├── balance.py
│ ├── deposit.py
│ ├── tip.py
│ ├── withdraw.py
│ ├── faucet.py
│ ├── faucet_balance.py
│ ├── top_holder.py
│ └── ...
├── core/
│ ├── command_handler/ # Folder fungsi internal terpisah
│ │ ├── tip.py
│ │ ├── withdraw.py
│ │ ├── balance.py
│ │ ├── deposit.py
│ │ ├── log_utils.py
│ │ └── init.py
│ ├── wallet_manager.py
│ └── user_manager.py
├── providers/ # Integrasi API per coin (BlockCypher, RPC, dll)
│ ├── blockcypher.py
│ └── ...
├── data/
│ ├── users.json # Menyimpan address + index setiap user
│ ├── transactions.log # Log internal tip, deposit, withdraw
├── config.py # Konfigurasi bot (TOKEN, API_PROVIDER, SUPPORTED_COINS)
└── README.md


## teknologi

* HD Wallet berbasis BIP44 (via `bip_utils`)
* Penyimpanan lokal untuk `users.json` dan `transactions.log`
* Logger sistem ke `data/bot.log`

## Instalasi

```bash
pip install -r requirements.txt
```

Isi `config.py` dengan:

```python
DISCORD_TOKEN = "TOKEN_DISCORD_KAMU"
API_PROVIDER = "blockcypher"  # atau "nownodes", "tatum"
BLOCKCYPHER_API_TOKEN = "..."
NOWNODES_API_KEY = "..."
TATUM_API_KEY = "..."
HD_WALLET_SEED = "seed phrase kamu yang aman"
```

## Menjalankan Bot

```bash
python3 bot.py
```

## Catatan Keamanan

* Jangan unggah `HD_WALLET_SEED` ke repositori publik.
* Gunakan file `.env` atau secrets manager di deployment production.

---

> Dibuat untuk bot Discord crypto skala ringan dengan dukungan multi-koin dan backend modular.

