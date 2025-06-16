"""
Пакет сервисов для работы с данными
"""

from .user_service import (
    load_user_data,
    save_user_data,
    get_user_id,
    register_user,
    get_all_users
)

from .subscription_service import (
    load_subscriptions,
    save_subscriptions,
    add_subscription,
    remove_subscription,
    get_subscribers,
    get_user_subscriptions
)

__all__ = [
    'load_user_data',
    'save_user_data',
    'get_user_id',
    'register_user',
    'get_all_users',
    'load_subscriptions',
    'save_subscriptions',
    'add_subscription',
    'remove_subscription',
    'get_subscribers',
    'get_user_subscriptions'
]