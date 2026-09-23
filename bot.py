from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os

TOKEN = os.getenv("BOT_TOKEN", "8859800843:AAGAs4cqC6q0FbdXAUvou7CHU4zIyP6uMnA")
ADMIN = int(os.getenv("ADMIN_ID", "7455322043"))
GROUP = os.getenv("GROUP_LINK", "https://chat.whatsapp.com/Dl6Q9RYdX2a2VpIwN7dA1G")

PAY_TEXT = "💳 PAY FOR MGP TRAINING\n\nOpay: 9063565356\nName: OGHENERO FAVOUR\nAmount: ₦2,000 (First 50: ₦1,500)"

async def start(update, ctx):
    kb = [[InlineKeyboardButton("YES", callback_data="yes"), InlineKeyboardButton("NO", callback_data="no")]]
    await update.message.reply_text("Welcome to GRAPHIC DESIGN TRAINING!\n\nMy name is GRP BOT\nAre you new to computers?", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update, ctx):
    q = update.callback_query
    await q.answer()
    if q.data in ["yes", "no"]:
        kb = [[InlineKeyboardButton("I Have Paid", callback_data="paid")]]
        await q.message.reply_text(PAY_TEXT, reply_markup=InlineKeyboardMarkup(kb))
    if q.data == "paid":
        await q.message.reply_text("Send your payment screenshot now. I will send group link automatically!")

async def receipt(update, ctx):
    await update.message.reply_text(f"✅ Payment received! Welcome!\n\nJoin here:\n{GROUP}\n\nSee you inside!")
    try:
        if update.effective_user.id != ADMIN:
            await ctx.bot.send_message(chat_id=ADMIN, text=f"New payment from {update.effective_user.full_name}")
            await ctx.bot.forward_message(chat_id=ADMIN, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except Exception as e:
        print(e)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, receipt))
    print("Bot 24/7 Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
