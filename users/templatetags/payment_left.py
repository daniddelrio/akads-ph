from django import template
from django.db.models import Sum
from users.models import Transaction
from users.services import get_amount_from_minutes

register = template.Library()


@register.simple_tag
def payment_left(user, payment):
    transactions = Transaction.objects.filter(user=user, payment=payment)
    if transactions.count() == 0:
        return payment.amount

    current_amount = transactions.aggregate(amount_paid=Sum("amount"))["amount_paid"]
    amount_needed = payment.amount - current_amount

    return amount_needed


@register.simple_tag
def get_amount(minutes):
    return get_amount_from_minutes(minutes)
