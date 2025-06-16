"""
Основной пакет Telegram-бота для загрузки Reels и Shorts
"""

# Импортируем основные компоненты для удобства
from .handlers import get_all_handlers
from .services import user_service, subscription_service

__all__ = ['handlers', 'services', 'utils', 'get_all_handlers']