import json
from django.core.exceptions import ObjectDoesNotExist

from carts.models import CartItem
from orders.models import Order, Payment

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
