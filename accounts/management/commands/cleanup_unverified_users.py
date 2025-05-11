from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import Account

class Command(BaseCommand):
    help = 'Cleans up unverified accounts and resets expired locks'

    def handle(self, *args, **options):
        # Delete old unverified accounts
        account_cutoff = timezone.now() - timedelta(days=7)
        old_accounts = Account.objects.filter(
            is_active=False,
            date_joined__lt=account_cutoff
        )
        deleted_count = old_accounts.count()
        old_accounts.delete()
        
        # Reset expired locks
        lock_cutoff = timezone.now()
        locked_accounts = Account.objects.filter(
            activation_locked_until__lte=lock_cutoff
        )
        reset_count = locked_accounts.update(
            activation_attempts=0,
            activation_locked_until=None
        )
        
        self.stdout.write(f"Deleted {deleted_count} unverified accounts and reset {reset_count} locks")