from django.http import HttpResponseRedirect
from django.urls import reverse

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page or raise error
            return HttpResponseRedirect(reverse('login'))  # or return HttpResponse("Unauthorized", status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
