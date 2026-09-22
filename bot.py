import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8009190498
GROUP_LINK = "https://chat.whatsapp.com/Dl6Q9RYdX2a2VpIwN7dA1G"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found! Check Render Environment Variables")

ACCOUNT_DETAILS = """💳 *PAY TO REGISTER FOR M.G.P TRAINING*

Opay: 9063565356
Name: OGHENERO FAVOUR
Amount: ₦2,000 (₦1,500 for first 50)

After payment, click 'I Have Paid' and send screenshot + full name."""

async def start(update, context):
    keyboard = [[InlineKeyboardButton("I Have Paid ✅", callback_data="paid")]]
    await update.message.reply_text(ACCOUNT_DETAILS, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def paid_callback(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Got it! Please send payment screenshot and your full name here.")

async def handle_message(update, context):
    user = update.effective_user
    text = f"New payment from {user.full_name} (@{user.username}) ID:{user.id}\n{update.message.text or ''}"
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)
        if update.message.photo:
            await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(f"Failed to forward to admin: {e}")
    await update.message.reply_text("Received! Admin will verify and send you WhatsApp group link soon.\n\n" + GROUP_LINK)

async def error_handler(update, context
