from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import RegistrationForm
from .service import register_user, send_activation_email, activate_user
from QCart.constants.error_message import ErrorMessage
from QCart.constants.success_message import SuccessMessage


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = register_user(form)  # Call service to handle registration
            if user:
                success, error = send_activation_email(user, request)  # Send activation email
                if not success:
                    messages.error(request, ErrorMessage.E00003.value)
                    print(error)
                    return redirect('register')

                return redirect('/accounts/login/?command=verification&email=' + user.email)
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

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
    success, error = activate_user(uidb64, token)  # Use service to handle account activation
    if success:
        messages.success(request, SuccessMessage.S00004.value)
        return redirect('login')
    else:
        messages.error(request, ErrorMessage.E00002.value)
        return redirect('register')