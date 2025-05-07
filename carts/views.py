from django.shortcuts import redirect, render
from carts.service import get_cart_data, get_product_by_id, remove_cart_item_from_cart, remove_cart_list_item_from_cart

# Create your views here.
def add_to_cart(request, product_id):
    get_product_by_id(request, product_id)  # Assuming you have a function to get product by ID
    return redirect('cart')  # Redirect to the cart page after adding the product

def remove_cart_item(request, product_id):
    remove_cart_item_from_cart(request, product_id)
    return redirect('cart')

def remove_list_cart_item(request, product_id):
    remove_cart_list_item_from_cart(request, product_id)
    return redirect('cart')

def cart(request):
    context = get_cart_data(request)
    return render(request, 'store/cart.html', context)


