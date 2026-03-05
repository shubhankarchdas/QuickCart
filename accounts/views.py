from accounts.models import Account, UserProfile
from .forms import UserProfileForm, UserForm, RegistrationForm
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate
from carts.service import associate_cart_items_with_user
from orders.models import Order, OrderProduct
from .forms import RegistrationForm
from .service import get_user_by_email, get_user_from_uid, handle_registration, is_token_valid, reset_user_password, send_activation_email, activate_user, send_password_reset_email
from QCart.constants.error_message import ErrorMessage
from QCart.constants.success_message import SuccessMessage
from .decorators import login_required_custom
import requests
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
            associate_cart_items_with_user(request, user)
            auth.login(request, user)
            messages.success(request, SuccessMessage.S00002.value)
            url = request.META.get('HttP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
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
    success, error, uid = activate_user(uidb64, token)
    if success:
        messages.success(request, SuccessMessage.S00004.value)
        user = Account.objects.get(pk=uid)
        auth.login(request, user)
        return redirect('login')
    else:
        messages.error(request, error or ErrorMessage.E00002.value)
        return redirect('register')


@login_required_custom
def dashboard(request):
    try:
        # Try to get userprofile, if it doesn't exist, create it
        userprofile, created = UserProfile.objects.get_or_create(user=request.user)
        
        order = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True) 
        order_count = order.count() 
        context = {
            'order_count': order_count, 
            'order': order, 
            'userprofile': userprofile
        } 
        return render(request, 'accounts/dashboard.html', context)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        messages.error(request, "An error occurred loading your dashboard.")
        return redirect('home')



def forgotPassword(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')  # or some other page

    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_user_by_email(email)

        if user:
            if request.user.is_active == False:
                messages.error(request, "Your account is not active yet. Please check your email for activation.")
                return redirect('login')

            send_password_reset_email(request, user)
            messages.success(request, SuccessMessage.S00005.value)
            return redirect('login')
        else:
            messages.error(request, ErrorMessage.E00005.value)
            return redirect('forgotPassword')

    return render(request, 'accounts/forgot_password.html')



def resetpassword_validate(request, uidb64, token):
    user = get_user_from_uid(uidb64)

    if user and is_token_valid(user, token):
        request.session['uid'] = user.pk
        request.session['reset_token'] = token
        messages.success(request, SuccessMessage.S00006.value)
        return redirect('resetPassword')
    else:
        messages.error(request, ErrorMessage.E00006.value)
        return redirect('login')


def resetPassword(request):
        # Ensure the user has an active account
    if not request.user.is_active:
        messages.error(request, "Your account is not active yet. Please check your email for activation.")
        return redirect('login')
    """Reset user password view, for authenticated users."""
    # Redirect logged-in users from reset password page (if unnecessary)
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in. No need to reset your password.")
        return redirect('dashboard')  # Redirect to dashboard or home page

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, ErrorMessage.E00004.value)
            return redirect('resetPassword')

        uid = request.session.get('uid')
        token = request.session.get('reset_token')

        success, error = reset_user_password(uid, token, password)

        if success:
            request.session.pop('uid', None)
            request.session.pop('reset_token', None)
            messages.success(request, "Password reset successfully.")
            return redirect('login')
        else:
            messages.error(request, error)
            return redirect('resetPassword')

    return render(request, 'accounts/reset_password.html')



@login_required_custom
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'accounts/my_orders.html', context)


@login_required_custom
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, SuccessMessage.S00007.value)
            return redirect('edit_profile')
        else:
            messages.error(request, ErrorMessage.E00007.value)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }    
    return render(request, 'accounts/edit_profile.html', context)


@login_required_custom
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password'] 
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, SuccessMessage.S00008.value)
                return redirect('change_password')
            
            else:
                messages.error(request, ErrorMessage.E00007.value)
                return redirect('change_password') 

        else:
            messages.error(request, ErrorMessage.E00004.value)
            return redirect('change_password')       

    return render(request, 'accounts/change_password.html')



@login_required_custom
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@require_POST
@csrf_exempt
def resend_activation(request):
    """AJAX view to resend activation email"""
    try:
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'})
        
        user = Account.objects.filter(email=email, is_active=False).first()
        if not user:
            return JsonResponse({'success': False, 'message': 'User not found or already activated'})
        
        # Check if user is locked
        if user.activation_locked_until and user.activation_locked_until > timezone.now():
            wait_minutes = (user.activation_locked_until - timezone.now()).seconds // 60
            return JsonResponse({
                'success': False, 
                'message': f'Too many attempts. Please wait {wait_minutes} minutes.'
            })
        
        # Send activation email
        success, msg = send_activation_email(user, request)
        
        if success:
            attempts_left = 3 - user.activation_attempts
            return JsonResponse({
                'success': True, 
                'message': msg,
                'attempts_left': attempts_left
            })
        else:
            return JsonResponse({'success': False, 'message': msg})
            
    except Exception as e:
        logger.error(f"Resend activation error: {str(e)}")
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})