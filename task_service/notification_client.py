import requests
from config import settings
import logging

logger = logging.getLogger(__name__)


def send_notification(user_id: int, message: str):
    """Send notification to notification service"""
    try:
        response = requests.post(
            f"{settings.NOTIFICATION_SERVICE_URL}/notify",
            json={"user_id": user_id, "message": message},
            timeout=5
        )
        if response.status_code == 200:
            logger.info(f"Notification sent for user {user_id}")
        else:
            logger.warning(f"Failed to send notification: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
