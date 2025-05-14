from django.shortcuts import get_object_or_404
from carts.models import Cart, CartItem
from store.models import Product

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def get_cart_data(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
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



def remove_cart_item_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass


def remove_cart_list_item_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  



#if a user add to cart before login, and then login, we need to associate the cart items with the user
def associate_cart_items_with_user(request, user):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                item.user = user
                item.save()
    except Cart.DoesNotExist:
        pass
