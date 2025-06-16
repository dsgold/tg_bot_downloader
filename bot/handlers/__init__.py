"""
Пакет обработчиков команд и сообщений бота
"""

from .base_handlers import get_base_handlers
from .subscription_handlers import get_subscription_handlers
from .admin_handlers import get_admin_handlers
from .video_handlers import get_video_handler

def get_all_handlers():
    """Возвращает все обработчики бота"""
    handlers = []
    handlers.extend(get_base_handlers())
    handlers.extend(get_subscription_handlers())
    handlers.extend(get_admin_handlers())
    handlers.append(get_video_handler())
    return handlers

__all__ = [
    'get_base_handlers',
    'get_subscription_handlers',
    'get_admin_handlers',
    'get_video_handler',
    'get_all_handlers'
]