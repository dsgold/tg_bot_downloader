import logging
import tempfile
import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
import yt_dlp
from bot.services import user_service, subscription_service
from bot.utils.config import COOKIES_FILE
from bot.utils.helpers import is_instagram_url


async def download_and_send_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    sender_username = user_service.register_user(user)

    if not sender_username:
        await update.message.reply_text("❌ У вас должен быть установлен username в Telegram")
        return

    url = update.message.text
    if not ("instagram.com/reel/" in url or "youtube.com/shorts/" in url):
        await update.message.reply_text("⚠️ Пожалуйста, отправьте ссылку на Instagram Reels или YouTube Shorts")
        return

    try:
        status_msg = await update.message.reply_text("⏳ Скачиваю видео...")
        await update.message.reply_chat_action("upload_video")

        with tempfile.TemporaryDirectory() as tmp_dir:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }

            if is_instagram_url(url) and os.path.exists(COOKIES_FILE):
                ydl_opts['cookiefile'] = COOKIES_FILE

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = ydl.prepare_filename(info)

            await status_msg.delete()

            with open(video_path, 'rb') as video_file:
                # Отправляем видео отправителю
                await update.message.reply_video(
                    video=video_file,
                    supports_streaming=True
                )

                # Отправляем видео подписчикам
                subscribers = subscription_service.get_subscribers(sender_username)
                for subscriber_username in subscribers:
                    subscriber_id = user_service.get_user_id(subscriber_username)
                    if subscriber_id:
                        try:
                            # Перематываем файл в начало
                            video_file.seek(0)
                            await context.bot.send_video(
                                chat_id=subscriber_id,
                                video=video_file,
                                supports_streaming=True,
                                caption=f"Видео от @{sender_username}"
                            )
                        except Exception as e:
                            logging.error(f"Ошибка отправки подписчику @{subscriber_username}: {e}")
                    else:
                        logging.warning(f"Подписчик @{subscriber_username} не найден")

    except Exception as e:
        logging.error(f"Ошибка обработки видео: {e}")
        error_msg = "❌ Произошла ошибка при обработке видео"
        if "cookies" in str(e).lower():
            error_msg += "\n\n⚠️ Для Instagram требуется авторизация. Добавьте файл cookies.txt"
        await update.message.reply_text(error_msg)


def get_video_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send_reel)