def is_instagram_url(url):
    from bot.utils.config import INSTAGRAM_DOMAINS
    return any(domain in url for domain in INSTAGRAM_DOMAINS)