from carts.models import Cart, CartItem
from carts.service import _cart_id
from store.forms import ReviewForm
from store.models import Product, ReviewRating, Variation  # if you're using a helper function for cart ID

def is_product_in_cart(request, product):
    return CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=product
    ).exists()


def get_product_by_id(request, product_id):
    return Product.objects.get(id=product_id)

def handle_add_to_cart(request, product):
    product = Product.objects.get(id=product.id)
    product_variation = []

    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                continue

    if request.user.is_authenticated:
        current_user = request.user

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list = []
            id_list = []

            for item in cart_items:
                existing_variation_list.append(list(item.variation.all()))
                id_list.append(item.id)

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(id=item_id)
                item.quantity += 1
                item.save()
            else:
                new_cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)  # Ensure quantity is 1
                if product_variation:
                    new_cart_item.variation.set(product_variation)
                new_cart_item.save()
        else:
            new_cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)  # Ensure quantity is 1
            if product_variation:
                new_cart_item.variation.set(product_variation)
            new_cart_item.save()

    else:
        # Guest user logic
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            existing_variation_list = []
            id_list = []

            for item in cart_items:
                existing_variation_list.append(list(item.variation.all()))
                id_list.append(item.id)

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(id=item_id)
                item.quantity += 1
                item.save()
            else:
                new_cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)  # Ensure quantity is 1
                if product_variation:
                    new_cart_item.variation.set(product_variation)
                new_cart_item.save()
        else:
            new_cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)  # Ensure quantity is 1
            if product_variation:
                new_cart_item.variation.set(product_variation)
            new_cart_item.save()




def get_existing_review(user_id, product_id):
    try:
        return ReviewRating.objects.get(user__id=user_id, product__id=product_id)
    except ReviewRating.DoesNotExist:
        return None


def update_review(instance, form_data):
    form = ReviewForm(form_data, instance=instance)
    if form.is_valid():
        form.save()
        return True
    return False


def create_review(form_data, user_id, product_id, ip):
    form = ReviewForm(form_data)
    if form.is_valid():
        data = ReviewRating(
            subject=form.cleaned_data['subject'],
            rating=form.cleaned_data['rating'],
            review=form.cleaned_data['review'],
            ip=ip,
            user_id=user_id,
            product_id=product_id
        )
        data.save()
        return True
    return False
