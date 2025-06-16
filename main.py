import logging
from telegram.ext import Application
from bot.utils.config import TOKEN
from bot.handlers.base_handlers import get_base_handlers
from bot.handlers.subscription_handlers import get_subscription_handlers
from bot.handlers.admin_handlers import get_admin_handlers
from bot.handlers.video_handlers import get_video_handler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    handlers = []
    handlers.extend(get_base_handlers())
    handlers.extend(get_subscription_handlers())
    handlers.extend(get_admin_handlers())
    handlers.append(get_video_handler())

    for handler in handlers:
        application.add_handler(handler)

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()