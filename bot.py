import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8009190498

*Define states*
WAITING_FOR_PROOF = 1

TEXT = "PAY TO REGISTER FOR M.G.P TRAINING

Opay: 9063565356
Name: OGHENERO FAVOUR
Amount: 2000

After payment, click I Have Paid"

async def start(update, context: ContextTypes.DEFAULT_TYPE)
btn = [[InlineKeyboardButton("I Have Paid", callback_data="paid")]]
await update.message.reply_text(TEXT, reply_markup=InlineKeyboardMarkup(btn))
return WAITING_FOR_PROOF

async def paid_cb(update, context: ContextTypes.DEFAULT_TYPE)
query = update.callback_query
await query.answer()
await query.message.reply_text("Please send your payment screenshot and full name now.")
return WAITING_FOR_PROOF

async def handle_proof(update, context: ContextTypes.DEFAULT_TYPE)
user = update.effective_user
msg = f"New payment proof from: {user.full_name} (@{user.username or 'No username'}, ID: {user.id})"

await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
if update.message.photo or update.message.document
await context.bot.forward_message(
chat_id=ADMIN_ID,
from_chat_id=update.effective_chat.id,
message_id=update.message.message_id
)

await update.message.reply_text("Received! Admin will verify soon. Join group: https://chat.whatsapp.com/Dl6Q9RYdX2a2VpIwN7dA1G")
return ConversationHandler.END

async def cancel(update, context: ContextTypes.DEFAULT_TYPE)
await update.message.reply_text("Process cancelled. Send /start whenever you are ready.")
return ConversationHandler.END

async def err(update, context: ContextTypes.DEFAULT_TYPE)
logging.error(context.error)

def main()
if not BOT_TOKEN
print("BOT_TOKEN missing")
return
app = Application.builder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
entry_points=[CommandHandler("start", start)],
states={
WAITING_FOR_PROOF: [
MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_proof)
]
},
fallbacks=[CommandHandler("cancel", cancel)]
)

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(paid_cb, pattern="^paid$"))
app.add_error_handler(err)

app.run_polling()

if __name__ == "__main__"
main()
```
