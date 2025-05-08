from django.http import HttpResponse
from django.shortcuts import redirect, render
from carts.models import Cart, CartItem
from carts.service import _cart_id, get_cart_data,remove_cart_item_from_cart, remove_cart_list_item_from_cart
from store.models import Product, Variation

# Create your views here.
def add_to_cart(request, product_id):
    product =  Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart  = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart  = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_validation = item.variation.all()
            existing_variation_list.append(list(existing_validation))
            id.append(item.id)

        if product_variation in existing_variation_list:
            #increase the quantity of the cart item
            index = existing_variation_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, cart=cart, id=item_id)
            item.quantity += 1
            item.save()
        else:
            #create a new cart item 
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity = 1, cart=cart,)
        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()
    return redirect('cart')  # Redirect to the cart page after adding the product

def remove_cart_item(request, product_id, cart_item_id):
    remove_cart_item_from_cart(request, product_id, cart_item_id)
    return redirect('cart')

def remove_list_cart_item(request, product_id, cart_item_id):
    remove_cart_list_item_from_cart(request, product_id, cart_item_id)
    return redirect('cart')

def cart(request):
    context = get_cart_data(request)
    return render(request, 'store/cart.html', context)


