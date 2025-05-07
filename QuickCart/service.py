from store.models import Product


def get_available_products():
    return Product.objects.filter(is_available=True).order_by('id')

def get_products_by_category(category):
    return get_available_products().filter(category=category)