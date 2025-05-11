from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import RegistrationForm
from .service import handle_registration, send_activation_email, activate_user
from QCart.constants.error_message import ErrorMessage
from QCart.constants.success_message import SuccessMessage
import logging
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Handle registration
                user, created, msg, error = handle_registration(form.cleaned_data)
                
                if error:
                    messages.error(request, msg)
                    return redirect('register')
                
                # Send activation email
                if user:
                    email_sent, email_error = send_activation_email(user, request)
                    if not email_sent:
                        messages.error(request, f"Failed to send activation email: {email_error or 'Unknown error'}")
                        if created:
                            user.delete()  # Clean up new user if email fails
                        return redirect('register')
                    
                    messages.success(request, msg)
                    return redirect(f'/accounts/login/?command=verification&email={user.email}')
                
                messages.error(request, msg)
                return redirect('register')
                
            except Exception as e:
                logger.error(f"Registration process failed: {str(e)}", exc_info=True)
                messages.error(request, "Registration failed due to system error. Please try again.")
                return redirect('register')
        
        # Form errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.title()}: {error}")
    
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, SuccessMessage.S00002.value)
            return redirect('home')
        else:
            messages.error(request, ErrorMessage.E00001.value)
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, SuccessMessage.S00003.value)
    return redirect('login')

def activate(request, uidb64, token):
    success, error = activate_user(uidb64, token)
    if success:
        messages.success(request, SuccessMessage.S00004.value)
        return redirect('login')
    else:
        messages.error(request, ErrorMessage.E00002.value)
        return redirect('register')