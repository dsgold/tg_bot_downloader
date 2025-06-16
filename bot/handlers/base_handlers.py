from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.services import user_service


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 <b>Доступные команды:</b>
/start - Начать работу с ботом
/help - Показать это сообщение
/subscribe [@username] - Подписаться на пользователя
/unsubscribe [@username] - Отписаться от пользователя
/mysubscriptions - Показать мои подписки
/mysubscribers - Показать кто на меня подписан
/users - Показать всех пользователей бота

📥 <b>Как использовать:</b>
Просто отправьте мне ссылку на:
- Instagram Reels
- YouTube Shorts
"""
    await update.message.reply_text(help_text, parse_mode="HTML")


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user_service.register_user(user)

    welcome_text = """
👋 <b>Привет! Я бот для загрузки Reels и Shorts</b>

🔹 Я могу скачивать видео из:
   • Instagram Reels
   • YouTube Shorts

🔹 <b>Как использовать:</b>
Отправь URL на видео!

🔹 <b>Система подписок:</b>
Вы можете подписаться на других пользователей с помощью /subscribe @username
Когда они отправляют видео - вы тоже его получите!
Если вас кто то доебал своими видео, то отписаться с помощью /unsubscribe @username
📌 /help для дебилов
"""
    await update.message.reply_text(welcome_text, parse_mode="HTML")


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = user_service.get_all_users()
    if not users:
        await update.message.reply_text("🤷 Пока нет зарегистрированных пользователей")
        return

    user_list = "\n".join([f"• @{user}" for user in users])
    await update.message.reply_text(f"👥 <b>Список троглодитов:</b>\n{user_list}", parse_mode="HTML")


def get_base_handlers():
    return [
        CommandHandler("start", handle_start),
        CommandHandler("help", help_command),
        CommandHandler("users", list_users)
    ]