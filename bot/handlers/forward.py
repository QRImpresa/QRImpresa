from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_OWNER_ID

# mappa: message_id_del_forward (in chat owner) -> chat_id_originale
user_map = {}

async def forward_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    # evita inoltrare messaggi inviati dall'owner a se stesso
    if update.effective_user and update.effective_user.id == BOT_OWNER_ID:
        return

    try:
        forwarded = await context.bot.forward_message(
            chat_id=BOT_OWNER_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        # salva mappa: il messaggio creato nella chat owner (forward) ha id forwarded.message_id
        # ma a volte la risposta dell'API diversa: usiamo forwarded.message_id se presente
        msg_id = forwarded.message_id if hasattr(forwarded, "message_id") else forwarded.message_id
        user_map[msg_id] = update.message.chat_id
    except Exception as e:
        # fallisce: log esterno (gestione in logger)
        print("Errore inoltro:", e)

    # conferma all'utente
    try:
        await update.message.reply_text("Messaggio ricevuto! Ti risponderemo a breve.")
    except Exception:
        pass
