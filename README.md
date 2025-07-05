# ?? Discord Tip Crypto Bot

Bot Discord untuk mengelola transaksi tip, deposit, balance, dan withdraw aset crypto seperti **BTC** dan **DOGE**.

## ? Fitur Utama

* `/tip @user SYMBOL AMOUNT` — kirim saldo secara internal ke pengguna lain
* `/withdraw SYMBOL ADDRESS AMOUNT` — tarik dana ke alamat blockchain
* `/balance SYMBOL` — cek saldo wallet on-chain
* `/deposit SYMBOL` — tampilkan alamat untuk menerima koin

## ?? Dukungan API Provider

Pluggable system — cukup atur `API_PROVIDER` di `config.py`:

* `blockcypher`
* `nownodes`
* `tatum`

## ?? Teknologi

* HD Wallet berbasis BIP44 (via `bip_utils`)
* Penyimpanan lokal untuk `users.json` dan `transactions.log`
* Logger sistem ke `data/bot.log`

## ??? Instalasi

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

## ?? Menjalankan Bot

```bash
python3 bot.py
```

## ?? Struktur Folder

```
discord-tip-bot/
+-- bot.py
+-- config.py
+-- core/
¦   +-- command_handler.py
¦   +-- user_manager.py
¦   +-- wallet_manager.py
+-- providers/
¦   +-- provider_base.py
¦   +-- blockcypher.py
¦   +-- nownodes.py
¦   +-- tatum.py
+-- utils/
¦   +-- crypto_utils.py
¦   +-- logger.py
+-- data/
¦   +-- users.json
¦   +-- transactions.log
¦   +-- bot.log
+-- requirements.txt
```

## ?? Catatan Keamanan

* Jangan unggah `HD_WALLET_SEED` ke repositori publik.
* Gunakan file `.env` atau secrets manager di deployment production.

---

> Dibuat untuk bot Discord crypto skala ringan dengan dukungan multi-koin dan backend modular.
