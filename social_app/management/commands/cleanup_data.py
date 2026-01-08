from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from social_app.models import Notification, Hashtag
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Clean up old data and optimize database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Number of days to keep notifications (default: 90)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        cutoff_date = timezone.now() - timedelta(days=days)

        self.stdout.write(f"Cleaning up data older than {days} days...")

        # Clean up old notifications
        old_notifications = Notification.objects.filter(
            created_at__lt=cutoff_date,
            is_read=True
        )
        notification_count = old_notifications.count()

        if dry_run:
            self.stdout.write(
                f"Would delete {notification_count} old read notifications"
            )
        else:
            deleted_count = old_notifications.delete()[0]
            self.stdout.write(
                self.style.SUCCESS(
                    f"Deleted {deleted_count} old read notifications"
                )
            )
            logger.info(f"Cleaned up {deleted_count} old notifications")

        # Clean up unused hashtags
        unused_hashtags = Hashtag.objects.filter(posts__isnull=True)
        hashtag_count = unused_hashtags.count()

        if dry_run:
            self.stdout.write(
                f"Would delete {hashtag_count} unused hashtags"
            )
        else:
            deleted_count = unused_hashtags.delete()[0]
            self.stdout.write(
                self.style.SUCCESS(
                    f"Deleted {deleted_count} unused hashtags"
                )
            )
            logger.info(f"Cleaned up {deleted_count} unused hashtags")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("This was a dry run. No data was actually deleted.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Data cleanup completed successfully!")
            )