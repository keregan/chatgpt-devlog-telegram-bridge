import requests

from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str) -> dict:
    if not TELEGRAM_BOT_TOKEN:
        return {
            "ok": False,
            "error": "TELEGRAM_BOT_TOKEN is not configured",
        }

    if not TELEGRAM_CHAT_ID:
        return {
            "ok": False,
            "error": "TELEGRAM_CHAT_ID is not configured",
        }

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10,
        )

        try:
            telegram_response = response.json()
        except ValueError:
            return {
                "ok": False,
                "status_code": response.status_code,
                "error": "Telegram returned a non-JSON response",
                "response_text": response.text[:500],
            }

        if response.ok and telegram_response.get("ok") is True:
            return {
                "ok": True,
                "status_code": response.status_code,
                "message": "Message sent to Telegram",
                "telegram_response": telegram_response,
            }

        return {
            "ok": False,
            "status_code": response.status_code,
            "error": "Telegram API returned an error",
            "telegram_response": telegram_response,
        }

    except requests.Timeout:
        return {
            "ok": False,
            "error": "Telegram API request timeout",
        }

    except requests.RequestException as error:
        return {
            "ok": False,
            "error": "Telegram API request failed",
            "details": str(error),
        }
