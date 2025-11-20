import logging
from typing import Optional

from app.core.celery_app import celery_app
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _send_sms(recipient: str, message: str) -> None:
    logger.info("Sending SMS to %s: %s", recipient, message)


def _send_email(recipient: str, message: str) -> None:
    logger.info("Sending Email to %s from %s: %s", recipient, settings.email_from, message)


def _send_telegram(recipient: str, message: str) -> None:
    logger.info("Sending Telegram message via bot %s to %s: %s", settings.telegram_bot_token, recipient, message)


def _send_websocket(channel: str, message: str) -> None:
    logger.info("Dispatching WebSocket update to %s: %s", channel, message)


@celery_app.task(name="app.services.notifications.dispatch_notification")
def dispatch_notification(channel: str, recipient: str, message: str) -> str:
    handlers = {
        "sms": _send_sms,
        "email": _send_email,
        "telegram": _send_telegram,
        "websocket": _send_websocket,
    }
    handler = handlers.get(channel)
    if not handler:
        raise ValueError(f"Unknown notification channel: {channel}")
    handler(recipient, message)
    return f"sent:{channel}"


class NotificationService:
    @staticmethod
    def queue_notification(channel: str, recipient: str, message: str):
        return dispatch_notification.delay(channel, recipient, message)

    @staticmethod
    def queue_booking_confirmation(recipient_phone: str, client_name: str, service_name: str):
        message = f"{client_name}, ваша запись на {service_name} подтверждена"
        NotificationService.queue_notification("sms", recipient_phone, message)
        NotificationService.queue_notification("telegram", recipient_phone, message)

    @staticmethod
    def queue_status_update(channel_id: str, status: str, plate_number: Optional[str] = None):
        message = f"Статус заказа обновлён: {status}"
        if plate_number:
            message = f"{plate_number}: {message}"
        NotificationService.queue_notification("websocket", channel_id, message)
