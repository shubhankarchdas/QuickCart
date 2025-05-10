from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .token import account_activation_token
from .models import Account
from QCart.constants.error_message import ErrorMessage

def register_user(form):
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    phone_number = form.cleaned_data['phone_number']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    username = email.split('@')[0]
    
    user = Account.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email,
        username=username,
        password=password
    )
    
    user.phone_number = phone_number
    user.is_active = False
    user.save()
    
    return user

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Please activate your account'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    send_email = EmailMessage(
        email_subject,
        message,
        to=[to_email]
    )
    
    try:
        send_email.send(fail_silently=False)
    except Exception as e:
        return False, str(e)
    
    return True, None

def activate_user(uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return True, None
    else:
        return False, "Invalid token or user"