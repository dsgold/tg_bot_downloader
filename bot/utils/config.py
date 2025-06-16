import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
COOKIES_FILE = "cookies.txt"
INSTAGRAM_DOMAINS = ["instagram.com", "www.instagram.com"]
USER_DATA_FILE = "data/users.json"
SUBSCRIPTIONS_FILE = "data/subscriptions.json"