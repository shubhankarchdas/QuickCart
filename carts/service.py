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
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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
    try:
        if request.user.is_authenticated:
            # For authenticated users, fetch cart items based on user and product
            cart_item = CartItem.objects.get(product_id=product_id, user=request.user, id=cart_item_id)
        else:
            # For guest users, fetch cart items based on session cart_id
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Ensure session cart exists
            cart_item = CartItem.objects.get(product_id=product_id, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except CartItem.DoesNotExist:
        # Handle the case where the cart item is not found, maybe log this or handle gracefully
        pass
    except Cart.DoesNotExist:
        # If the cart does not exist (for session-based or user-based carts), handle the error
        pass



def remove_cart_list_item_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  



def associate_cart_items_with_user(request, user):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(cart=cart)
            product_variation = []
            for item in cart_items:
                existing_variation = item.variation.all()
                product_variation.append(list(existing_variation))

            user_cart_items = CartItem.objects.filter(user=user)
            existing_variation_list = []
            id_list = []

            for item in user_cart_items:
                existing_variation_list.append(list(item.variation.all()))
                id_list.append(item.id)

            for pr in product_variation:
                if pr in existing_variation_list:
                    index = existing_variation_list.index(pr)
                    item_id = id_list[index]
                    item = CartItem.objects.get(id=item_id)
                    item.quantity += 1
                    item.save()
                else:
                    # Create a new CartItem, ensuring that the 'product' field is set
                    # Find the corresponding product for the cart item
                    product = cart_items.first().product  # Assuming all items in the cart have the same product

                    # Ensure product is not null before creating the CartItem
                    if product:
                        cart_item = CartItem.objects.create(cart=cart, user=user, quantity=1, product=product)
                        for variation in pr:
                            cart_item.variation.add(variation)
                        cart_item.save()
                    else:
                        # Handle the case where product is null, if necessary
                        pass
    except Cart.DoesNotExist:
        pass
