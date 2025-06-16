import json
import os
from bot.utils.config import USER_DATA_FILE


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_user_data(data):
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user_id(username):
    users = load_user_data()
    user_data = users.get(username.lower()) if username else None
    return user_data["id"] if user_data else None


def register_user(user):
    if not user.username:
        return None

    users = load_user_data()
    username_lower = user.username.lower()
    users[username_lower] = {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name
    }
    save_user_data(users)
    return username_lower


def get_all_users():
    users = load_user_data()
    return list(users.keys())