from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = BOT_TOKEN = "8900190498:AAHH7TydVST-bJKkwyKizVAMnDMe7oqf7ig"
ADMIN_ID = 8900190498
GROUP_LINK = "https://chat.whatsapp.com/FUTP2GGcc5tIb6Jk1K3tTr"

ACCOUNT_DETAILS = """
💳 **PAY TO REGISTER FOR M.G.P TRAINING:**

**Opay: 9063565536**
**Name: OGHENERO FAVOUR**

Amount: ₦2,000

After payment, click "I Have Paid" below and upload your payment screenshot.
"""

async def start(update, context):
    keyboard = [[InlineKeyboardButton("✅ I Have Paid", callback_data='paid')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(ACCOUNT_DETAILS, reply_markup=reply_markup, parse_mode='Markdown')

async def paid_callback(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Great! Abeg send your payment screenshot / receipt now. I go forward am to admin for verification.")

async def handle_photo(update, context):
    user = update.effective_user
    # Forward to admin
    caption = f"🔔 New Payment from @{user.username or user.first_name}\nID: {user.id}\nName: {user.full_name}"
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption)

    # Create approve buttons
    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f'approve_{user.id}'),
         InlineKeyboardButton("❌ Decline", callback_data=f'decline_{user.id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"Approve this user? ID: {user.id}", reply_markup=reply_markup)

    await update.message.reply_text("✅ Screenshot received! Admin go verify am shortly. You go get WhatsApp group link once approved.")

async def handle_approval(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('approve_'):
        user_id = int(data.split('_')[1])
        try:
            await context.bot.send_message(chat_id=user_id, text=f"🎉 CONGRATULATIONS! Your payment has been APPROVED!\n\nHere is your private WhatsApp group link:\n{GROUP_LINK}\n\nJoin now for M.G.P Training!")
            await query.edit_message_text(f"✅ Approved user {user_id}")
        except:
            await query.edit_message_text(f"User {user_id} never start bot, but approved.")

    elif data.startswith('decline_'):
        user_id = int(data.split('_')[1])
        try:
            await context.bot.send_message(chat_id=user_id, text="❌ Sorry, your payment could not be verified. Please send a clearer screenshot or contact admin.")
        except:
            pass
        await query.edit_message_text(f"❌ Declined user {user_id}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(paid_callback, pattern='^paid$'))
    app.add_handler(CallbackQueryHandler(handle_approval, pattern='^(approve|decline)_'))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print(f"Bot is running... for @ainovum_ai_bot")
    app.run_polling()

if __name__ == '__main__':
    main()