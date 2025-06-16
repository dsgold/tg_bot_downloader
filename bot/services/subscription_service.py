import json
import os
from bot.utils.config import SUBSCRIPTIONS_FILE


def load_subscriptions():
    if os.path.exists(SUBSCRIPTIONS_FILE):
        try:
            with open(SUBSCRIPTIONS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_subscriptions(subscriptions):
    os.makedirs(os.path.dirname(SUBSCRIPTIONS_FILE), exist_ok=True)
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subscriptions, f, indent=2)


def add_subscription(subscriber_username, target_username):
    subscriptions = load_subscriptions()
    subscriber_key = subscriber_username.lower()
    target_key = target_username.lower()

    if subscriber_key not in subscriptions:
        subscriptions[subscriber_key] = []

    if target_key not in subscriptions[subscriber_key]:
        subscriptions[subscriber_key].append(target_key)
        save_subscriptions(subscriptions)
        return True
    return False


def remove_subscription(subscriber_username, target_username):
    subscriptions = load_subscriptions()
    subscriber_key = subscriber_username.lower()
    target_key = target_username.lower()

    if subscriber_key in subscriptions and target_key in subscriptions[subscriber_key]:
        subscriptions[subscriber_key].remove(target_key)
        save_subscriptions(subscriptions)
        return True
    return False


def get_subscribers(target_username):
    subscriptions = load_subscriptions()
    target_key = target_username.lower()
    return [user for user, subs in subscriptions.items() if target_key in subs]


def get_user_subscriptions(username):
    subscriptions = load_subscriptions()
    return subscriptions.get(username.lower(), [])

def get_user_subscribers(username):
    subscriptions = load_subscriptions()
    username_lower = username.lower()
    return [user for user, subs in subscriptions.items() if username_lower in [s.lower() for s in subs]]