# utils/logger.py
import logging
import os

LOG_FILE = "data/bot.log"

# Pastikan direktori ada
os.makedirs("data", exist_ok=True)

# Setup logger
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

def log_info(message: str):
    logging.info(message)

def log_warning(message: str):
    logging.warning(message)

def log_error(message: str):
    logging.error(message)

def log_debug(message: str):
    logging.debug(message)
