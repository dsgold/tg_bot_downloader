from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.services import subscription_service
from bot.utils.config import ADMIN_CHAT_ID


async def admin_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Доступ запрещен")
        return

    subscriptions = subscription_service.load_subscriptions()
    if not subscriptions:
        await update.message.reply_text("🤷 Нет активных подписок")
        return

    report = []
    for subscriber, targets in subscriptions.items():
        if targets:
            report.append(f"👤 @{subscriber} подписан на:")
            report.extend([f"   → @{target}" for target in targets])

    await update.message.reply_text("\n".join(report))


def get_admin_handlers():
    return [
        CommandHandler("allsubscriptions", admin_subscriptions)
    ]