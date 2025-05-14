from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six  # For Python 2/3 compatibility if needed (or use str() directly in Python 3)
import hashlib

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) +
            str(timestamp) +
            str(user.is_active) +
            str(user.password)
        )

    def make_token(self, user):
        # Optionally override to change token formatting logic
        return super().make_token(user)

    def check_token(self, user, token):
        return super().check_token(user, token)

account_activation_token = AccountActivationTokenGenerator()
