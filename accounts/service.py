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

def handle_registration(form_data):
    """Handle registration with attempt tracking"""
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
            
            return user, created, None, None
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return None, False, "Registration error occurred.", str(e)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None, False, "Registration failed.", str(e)

def send_activation_email(user, request):
    """Send activation email with attempt limiting"""
    try:
        # Check if user can send activation
        can_send, msg = user.can_send_activation()
        if not can_send:
            return False, msg
        
        # Check attempt limit
        if user.activation_attempts >= 2:
            user.activation_locked_until = timezone.now() + timedelta(minutes=5)
            user.save()
            return False, "Maximum attempts reached. Please wait 5 minutes."
        
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
        user.last_activation_sent = timezone.now()
        user.activation_attempts += 1
        user.save()
        
        attempts_left = 2 - user.activation_attempts
        if attempts_left > 0:
            return True, f"Activation email sent! You have {attempts_left} attempt{'s' if attempts_left > 1 else ''} left."
        return True, "Activation email sent!"
        
    except Exception as e:
        logger.error(f"Email error: {str(e)}")
        return False, "Failed to send activation email."

def activate_user(uidb64, token):
    """Activate user account"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.reset_activation_attempts()  # Reset on successful activation
            user.save()
            return True, None
        return False, "Invalid token"
    except Exception as e:
        logger.error(f"Activation error: {str(e)}")
        return False, "Invalid activation link" 