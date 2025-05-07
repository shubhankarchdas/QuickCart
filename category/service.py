from django.shortcuts import get_object_or_404
from store.models import Product
from .models import Category
from django.db.models import Q

def get_category_by_slug(slug):
    return get_object_or_404(Category, slug=slug)

def get_all_categories():
    return Category.objects.all()

def get_product_by_category_and_slug(category_slug, product_slug):
    category = get_category_by_slug(category_slug)
    return get_object_or_404(Product, category__slug=category_slug, slug=product_slug)


def search_products(keyword):
    if not keyword:
        return Product.objects.none()

    return Product.objects.filter(
        Q(product_name__icontains=keyword) |
        Q(description__icontains=keyword)
    ).order_by('-updated_at') 
    