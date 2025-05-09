from django.http import HttpResponse
from django.shortcuts import redirect, render
from carts.service import get_cart_data,remove_cart_item_from_cart, remove_cart_list_item_from_cart
from store.service import get_product_by_id, handle_add_to_cart

def add_to_cart(request, product_id):
    product = get_product_by_id(request, product_id)
    handle_add_to_cart(request, product)
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    remove_cart_item_from_cart(request, product_id, cart_item_id)
    return redirect('cart')

def remove_list_cart_item(request, product_id, cart_item_id):
    remove_cart_list_item_from_cart(request, product_id, cart_item_id)
    return redirect('cart')

def cart(request):
    context = get_cart_data(request)
    return render(request, 'store/cart.html', context)


