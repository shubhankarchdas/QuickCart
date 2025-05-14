from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import RegistrationForm
from .service import handle_registration, send_activation_email, activate_user
from QCart.constants.error_message import ErrorMessage
from QCart.constants.success_message import SuccessMessage
from .decorators import login_required_custom
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Handle registration
                user, created, error_msg, error = handle_registration(form.cleaned_data)
                
                if error_msg:
                    messages.error(request, error_msg)
                    return redirect('register')
                
                # Send activation email
                if user:
                    success, msg = send_activation_email(user, request)
                    if not success:
                        messages.error(request, msg)
                        if created:
                            user.delete()
                        return redirect('register')
                    
                    messages.success(request, msg)
                    return redirect(f'/accounts/login/?command=verification&email={user.email}')
                
                messages.error(request, "Registration failed")
                return redirect('register')
                
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                messages.error(request, "Registration failed. Please try again.")
                return redirect('register')
        
        # Form errors
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(request, f"{field}: {error}")
                else:
                    messages.error(request, f"{error}")
    
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


@login_required_custom
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
        messages.error(request, error or ErrorMessage.E00002.value)
        return redirect('register')


@login_required_custom
def dashboard(request):   
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    return render(request, 'accounts/forgot_password.html')