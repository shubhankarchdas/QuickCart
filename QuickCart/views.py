from django.shortcuts import render
from store.models import Product
from category.models import Category


def home(request):
    # All available products
    products = Product.objects.filter(is_available=True)

    # New arrivals (latest 8)
    new_products = Product.objects.filter(
        is_available=True
    ).order_by('-created_at')[:8]

    # Featured products (latest 8)
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    ).order_by('-created_at')[:8]

    # Get categories safely
    women_category = Category.objects.filter(slug='women').first()
    men_category = Category.objects.filter(slug='men').first()

    # Default fallback URLs
    women_url = '/store/'
    men_url = '/store/'

    # If category exists, generate correct URL
    if women_category:
        women_url = f'/store/category/{women_category.slug}/'

    if men_category:
        men_url = f'/store/category/{men_category.slug}/'

    context = {
        'products': products,
        'new_products': new_products,
        'featured_products': featured_products,
        'women_url': women_url,
        'men_url': men_url,
    }

    return render(request, 'home.html', context)