from django.shortcuts import render
from store.models import ReviewRating,Product
from .service import get_available_products

# Create your views here.
def home(request):
    products = get_available_products()
    
    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context = {
        'products': products,
        'reviews' : reviews,
    }
    return render(request, 'home.html', context)

