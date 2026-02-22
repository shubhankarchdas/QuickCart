from django.shortcuts import render
from store.models import Product
from category.models import Category


def home(request):
    # Products
    products = Product.objects.filter(is_available=True)

    new_products = Product.objects.filter(
        is_available=True
    ).order_by('-created_at')[:8]

    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    ).order_by('-created_at')[:8]

    # Women & Men categories for Shop Now
    women_category = Category.objects.filter(slug='women').first()
    men_category = Category.objects.filter(slug='men').first()

    women_url = women_category.get_url() if women_category else '/store/'
    men_url = men_category.get_url() if men_category else '/store/'

    # ONLY 8 custom selected categories
    slider_categories = Category.objects.filter(
        is_featured=True
    )[:8]

    context = {
        'products': products,
        'new_products': new_products,
        'featured_products': featured_products,
        'slider_categories': slider_categories,
        'women_url': women_url,
        'men_url': men_url,
    }

    return render(request, 'home.html', context)



def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def blog(request):
    return render(request, 'pages/blog.html')

def faq(request):
    return render(request, 'policies/faq.html')

def shipping_policy(request):
    return render(request, 'policies/shipping_policy.html')

def return_policy(request):
    return render(request, 'policies/return_policy.html')

def privacy_policy(request):
    return render(request, 'policies/privacy_policy.html')

def terms(request):
    return render(request, 'policies/terms.html')