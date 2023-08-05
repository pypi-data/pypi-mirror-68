from django.conf import settings
from django.core import management

from .util.core_helpers import celery_optional
from .util.notifications import send_notification as _send_notification


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
    """Send a notification object to its recipient.

    :param notification: primary key of the notification object to send
    :param resend: Define whether to also send if the notification was already sent
    """
    _send_notification(notification, resend)


@celery_optional
def backup_data() -> None:
    """Backup database and media using django-dbbackup."""
    # Assemble command-line options for dbbackup management command
    db_options = "-z " * settings.DBBACKUP_COMPRESS_DB + "-e" * settings.DBBACKUP_ENCRYPT_DB
    media_options = (
        "-z " * settings.DBBACKUP_COMPRESS_MEDIA + "-e" * settings.DBBACKUP_ENCRYPT_MEDIA
    )

    # Hand off to dbbackup's management commands
    management.call_command("dbbackup", db_options)
    management.call_command("mediabackup", media_options)
