from django.shortcuts import get_object_or_404
from carts.models import Cart, CartItem
from store.models import Product

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def get_product_by_id(request, product_id):
    product =  Product.objects.get(id=product_id)

    try:
        cart  = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart  = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()
    return cart_item


def get_cart_data(request):
    total = 0
    quantity = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (total * 2)/100  
        grand_total = total + tax 
    except Cart.DoesNotExist:
        pass

    return {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }



def remove_cart_item_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass


def remove_cart_list_item_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass    