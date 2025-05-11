from datetime import timedelta
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Account
from .token import account_activation_token
import logging

logger = logging.getLogger(__name__)

from django.db import IntegrityError
from django.core.exceptions import ValidationError


def handle_registration(form_data):
    """
    Handles the complete registration flow with robust error handling
    Returns: (user, is_new_user, message, error)
    """
    try:
        email = form_data['email']
        
        # Check for existing verified user
        if Account.objects.filter(email=email, is_active=True).exists():
            return None, False, "An account with this email already exists.", None
        
        # Get or create unverified user
        try:
            user, created = Account.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': form_data['first_name'],
                    'last_name': form_data['last_name'],
                    'phone_number': form_data['phone_number'],
                    'is_active': False,
                }
            )
            
            # Update existing unverified user
            if not created:
                user.first_name = form_data['first_name']
                user.last_name = form_data['last_name']
                user.phone_number = form_data['phone_number']
                user.set_password(form_data['password'])
                user.save()
            
            message = "Registration successful! Please check your email." if created else \
                     "We've sent you another activation link."
            return user, created, message, None
            
        except IntegrityError as e:
            logger.error(f"Integrity error during registration: {str(e)}")
            return None, False, "Database error occurred. Please try again.", str(e)
            
    except Exception as e:
        logger.error(f"Unexpected error in handle_registration: {str(e)}", exc_info=True)
        return None, False, "Registration failed due to system error.", str(e)

def send_activation_email(user, request):
    """Send activation email with comprehensive error handling"""
    try:
        # Ensure required attributes exist
        if not hasattr(user, 'email'):
            raise ValueError("Invalid user object provided")
            
        # Rate limiting check
        if hasattr(user, 'last_activation_sent'):
            if user.last_activation_sent and (timezone.now() - user.last_activation_sent).total_seconds() < 300:
                logger.warning(f"Activation email rate limit reached for {user.email}")
                return False, "Please wait before requesting another activation email"

        # Prepare and send email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send(fail_silently=False)
        
        # Update tracking
        if hasattr(user, 'last_activation_sent'):
            user.last_activation_sent = timezone.now()
        if hasattr(user, 'activation_attempts'):
            user.activation_attempts += 1
        user.save()
        
        return True, None
        
    except Exception as e:
        logger.error(f"Failed to send activation email: {str(e)}", exc_info=True)
        return False, str(e)

def activate_user(uidb64, token):
    """Activate user account using uid and token"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return True, None
        return False, "Invalid activation token"
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
        logger.error(f"Activation error: {str(e)}")
        return False, "Invalid activation link"