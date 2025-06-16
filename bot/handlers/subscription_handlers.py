from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.services import user_service, subscription_service


async def my_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user_service.register_user(user)

    if not username:
        await update.message.reply_text("❌ У вас должен быть установлен username в Telegram")
        return

    subscriptions = subscription_service.get_user_subscriptions(username)
    if not subscriptions:
        await update.message.reply_text("🤷 Вы пока ни на кого не подписаны")
        return

    sub_list = "\n".join([f"• @{sub}" for sub in subscriptions])
    await update.message.reply_text(f"⭐ <b>Ваши подписки:</b>\n{sub_list}", parse_mode="HTML")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    subscriber_username = user_service.register_user(user)

    if not subscriber_username:
        await update.message.reply_text("❌ У вас должен быть установлен username в Telegram")
        return

    # Если не указан пользователь - покажем список доступных (исключая себя)
    if not context.args:
        all_users = user_service.get_all_users()
        # Исключаем текущего пользователя из списка
        available_users = [u for u in all_users if u.lower() != subscriber_username]

        if not available_users:
            await update.message.reply_text("🤷 Пока нет других пользователей для подписки")
            return

        user_list = "\n".join([f"• /subscribe @{user}" for user in available_users])
        await update.message.reply_text(
            f"👥 <b>Доступные пользователи для подписки:</b>\n\n{user_list}\n\n"
            "Используйте: <code>/subscribe @username</code>",
            parse_mode="HTML"
        )
        return

    target_username = context.args[0].lstrip('@')
    if not target_username:
        await update.message.reply_text("⚠️ Неверный формат username")
        return

    # Нельзя подписаться на себя
    if target_username.lower() == subscriber_username:
        await update.message.reply_text("🤔 Нельзя подписаться на самого себя")
        return

    # Проверяем, зарегистрирован ли целевой пользователь
    if not user_service.get_user_id(target_username):
        await update.message.reply_text("❌ Этот пользователь еще не зарегистрирован в боте")
        return

    if subscription_service.add_subscription(subscriber_username, target_username):
        await update.message.reply_text(f"✅ Вы подписались на @{target_username}")
    else:
        await update.message.reply_text(f"❌ Вы уже подписаны на @{target_username}")


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    subscriber_username = user_service.register_user(user)

    if not subscriber_username:
        await update.message.reply_text("❌ У вас должен быть установлен username в Telegram")
        return

    if not context.args:
        subscriptions = subscription_service.get_user_subscriptions(subscriber_username)
        if not subscriptions:
            await update.message.reply_text("🤷 У вас нет активных подписок")
            return

        sub_list = "\n".join([f"• /unsubscribe @{sub}" for sub in subscriptions])
        await update.message.reply_text(
            f"⭐ <b>Ваши текущие подписки:</b>\n\n{sub_list}\n\n"
            "Используйте: <code>/unsubscribe @username</code>",
            parse_mode="HTML"
        )
        return

    target_username = context.args[0].lstrip('@')
    if not target_username:
        await update.message.reply_text("⚠️ Неверный формат username")
        return

    if subscription_service.remove_subscription(subscriber_username, target_username):
        await update.message.reply_text(f"✅ Вы отписались от @{target_username}")
    else:
        await update.message.reply_text(f"❌ Вы не подписаны на @{target_username}")


async def my_subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user_service.register_user(user)

    if not username:
        await update.message.reply_text("❌ У вас должен быть установлен username в Telegram")
        return

    subscribers = subscription_service.get_user_subscribers(username)

    if not subscribers:
        await update.message.reply_text("🤷 У вас пока нет подписчиков")
        return

    subscribers_list = "\n".join([f"• @{sub}" for sub in subscribers])
    await update.message.reply_text(
        f"👥 <b>Ваши подписчики:</b>\n{subscribers_list}",
        parse_mode="HTML"
    )

def get_subscription_handlers():
    return [
        CommandHandler("mysubscriptions", my_subscriptions),
        CommandHandler("mysubscribers", my_subscribers),
        CommandHandler("subscribe", subscribe),
        CommandHandler("unsubscribe", unsubscribe)
    ]