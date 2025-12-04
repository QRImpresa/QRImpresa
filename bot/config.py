import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID") or 0)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN non trovato: impostalo in .env o come secret TELEGRAM_BOT_TOKEN")
if BOT_OWNER_ID == 0:
    raise RuntimeError("BOT_OWNER_ID non impostato. Inserisci il tuo Telegram ID in .env o come secret BOT_OWNER_ID")
