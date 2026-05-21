import requests

from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str) -> dict:
    if not TELEGRAM_BOT_TOKEN:
        return {
            "status": "skipped",
            "message": "Telegram bot token is not configured"
        }

    if not TELEGRAM_CHAT_ID:
        return {
            "status": "skipped",
            "message": "Telegram chat id is not configured"
        }

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }

    response = requests.post(url, json=payload, timeout=10)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": response.text
        }

    return {
        "status": "sent",
        "message": "Message sent to Telegram"
    }