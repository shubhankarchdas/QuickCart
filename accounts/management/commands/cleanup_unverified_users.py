from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import Account

class Command(BaseCommand):
    help = 'Deletes unverified accounts older than 7 days'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=7)
        old_unverified = Account.objects.filter(
            is_active=False,
            date_joined__lt=cutoff
        )
        count = old_unverified.count()
        old_unverified.delete()
        self.stdout.write(f"Deleted {count} unverified accounts")