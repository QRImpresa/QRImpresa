from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_OWNER_ID
from handlers.forward import user_map

async def owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # permetti solo al proprietario
    if not update.effective_user or update.effective_user.id != BOT_OWNER_ID:
        return

    # deve essere una risposta a un messaggio inoltrato
    if not update.message or not update.message.reply_to_message:
        return

    reply_to = update.message.reply_to_message
    # il messaggio a cui l'owner ha risposto si trova nella chat owner => abbiamo il suo message_id
    msg_id = reply_to.message_id

    # trova l'utente originale
    user_chat_id = user_map.get(msg_id)
    if not user_chat_id:
        await update.message.reply_text("Non riesco a trovare l'utente originale.")
        return

    # invia testo (se presente)
    try:
        if update.message.text:
            await context.bot.send_message(chat_id=user_chat_id, text=update.message.text)
        # inoltra media se presente
        elif update.message.photo:
            # prendi l'ultima photo del messaggio
            await context.bot.send_photo(chat_id=user_chat_id, photo=update.message.photo[-1].file_id, caption=update.message.caption or "")
        elif update.message.document:
            await context.bot.send_document(chat_id=user_chat_id, document=update.message.document.file_id, caption=update.message.caption or "")
        else:
            await update.message.reply_text("Tipo di contenuto non supportato per la risposta automatica.")
            return
        await update.message.reply_text("Risposta inviata all'utente.")
    except Exception as e:
        await update.message.reply_text(f"Errore nell'invio: {e}")
