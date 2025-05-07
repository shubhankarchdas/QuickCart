from carts.models import CartItem
from carts.service import _cart_id  # if you're using a helper function for cart ID

def is_product_in_cart(request, product):
    return CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=product
    ).exists()
