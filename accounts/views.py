from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate
from QCart.constants.error_message import ErrorMessage
from QCart.constants.success_message import SuccessMessage
from accounts.models import Account
from .forms import RegistrationForm


# verify email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .token import account_activation_token

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
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
            current_site = get_current_site(request)
            email_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_eamil = form.cleaned_data.get('email')
            send_email = EmailMessage(
                email_subject,
                message,
                to=[to_eamil]
            )
            try:
                send_email.send(fail_silently=False)
            except Exception as e:
                messages.error(request, ErrorMessage.E00003.value)
                print(e)
                return redirect('register')


            # messages.success(request, SuccessMessage.S00001.value)
            return redirect('/accounts/login/?command=verification&email='+email)
        else:
            print(form.errors) 
    else:
        form = RegistrationForm()    
    context = {
        'form': form,
    }
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



#decorator to check if user is logged in
def logout(request):
    auth.logout(request)
    messages.success(request, SuccessMessage.S00003.value)
    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, SuccessMessage.S00004.value)
        return redirect('login')
    else:
        messages.error(request, ErrorMessage.E00002.value)
        return redirect('register')