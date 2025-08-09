import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from carts.models import CartItem
from orders.models import Order, Payment, OrderProduct
from store.models import Product

def process_payment_data(user, payment_data):
    """
    Processes payment data and updates the Order and Payment models.

    Args:
        user (User): The current logged-in user.
        payment_data (dict): Dictionary containing payment details.

    Returns:
        Order: The updated order instance.

    Raises:
        ObjectDoesNotExist: If the order matching the criteria is not found.
    """
    order = Order.objects.get(user=user, is_ordered=False, order_number=payment_data['orderID'])

    payment = Payment.objects.create(
        user=user,
        payment_id=payment_data['transID'],
        payment_method=payment_data['payment_method'],
        amount_paid=order.total,
        status=payment_data['status']
    )

    order.payment = payment
    order.is_ordered = True
    order.save()

    return order


def complete_order_processing(user, order, payment):
    """
    Handles cart-to-order conversion, stock update, cart clear, and email sending.
    """
    cart_items = CartItem.objects.filter(user=user)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        # Set variations
        product_variation = item.variations.all()
        order_product.variations.set(product_variation)
        order_product.save()

        # Reduce stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear user's cart
    CartItem.objects.filter(user=user).delete()

    # Send confirmation email
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': user,
        'order': order,
    })
    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()