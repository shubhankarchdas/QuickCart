from django.shortcuts import render
from .service import get_available_products

# Create your views here.
def home(request):
    products = get_available_products()
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)




# 59 min 19 sec