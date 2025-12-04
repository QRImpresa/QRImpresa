import asyncio
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from config import BOT_TOKEN, BOT_OWNER_ID
from handlers.forward import forward_to_owner
from handlers.owner_reply import owner_reply
from utils.logger import setup_logger

logger = setup_logger("qrimpresa-bot")

async def main():
    logger.info("Avvio bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # handler: owner replies (solo messaggi di testo che sono reply e provengono dall'owner)
    app.add_handler(MessageHandler(filters.User(BOT_OWNER_ID) & filters.REPLY & filters.TEXT, owner_reply))

    # handler: tutti gli altri messaggi (forward a owner)
    app.add_handler(MessageHandler(~filters.User(BOT_OWNER_ID), forward_to_owner))

    # Avvia polling
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot fermato manualmente.")
