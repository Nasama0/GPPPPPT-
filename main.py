# main.py
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from tv_ideas_scraper import get_tv_ideas
from config import TELEGRAM_TOKEN, MONITORS

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📊 TradingView Ідеї", callback_data='tv_ideas')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привіт, Зайко! 🔮 Обери дію:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'tv_ideas':
        response = get_tv_ideas_summary()
        await query.edit_message_text(response, parse_mode='HTML', disable_web_page_preview=True)

def get_tv_ideas_summary():
    message = "🧠 <b>TradingView Ідеї</b>\n"
    from tv_ideas_scraper import get_tv_ideas
    for coin in MONITORS:
        ideas = get_tv_ideas(coin)
        if ideas:
            idea = ideas[0]
            message += f"\n🪙 <b>{coin}</b>\n"
            message += f"{idea['title']}\n"
            message += f"✍️ {idea['author']} — <i>{idea['sentiment']}</i>\n"
            message += f"🔗 <a href='{idea['link']}'>Переглянути</a>\n"
    return message

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_click))
    logging.info("🚀 Бот запущено!")
    app.run_polling()

if __name__ == '__main__':
    main()
