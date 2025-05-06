from django.shortcuts import render
from QuickCart.service import get_available_products, get_products_by_category
from category.service import get_category_by_slug, get_product_by_category_and_slug

def store(request, category_slug=None):
    if category_slug:
        category = get_category_by_slug(category_slug)
        products = get_products_by_category(category)
    else:
        products = get_available_products()

    context = {
        'products': products,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = get_product_by_category_and_slug(category_slug, product_slug)
    
    context = {
        'single_product': single_product,
        'category': single_product.category,
    }

    return render(request, 'store/product_detail.html', context)