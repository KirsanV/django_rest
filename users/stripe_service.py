import os
import stripe
from django.conf import settings


STRIPE_API_KEY = getattr(settings, 'STRIPE_API_KEY', os.environ.get('STRIPE_API_KEY'))
stripe.api_key = STRIPE_API_KEY


def create_product(name):
    product = stripe.Product.create(name=name)
    return product['id']


def create_price(product_id, amount_cents, currency='rub'):
    price = stripe.Price.create(
        unit_amount=amount_cents,
        currency=currency,
        product=product_id
    )
    return price['id']


def create_checkout_session(price_id, success_url, cancel_url, mode='payment'):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': price_id, 'quantity': 1}],
        mode=mode,
        success_url=success_url,
        cancel_url=cancel_url
    )
    return {'id': session['id'], 'url': session['url']}


def prepare_payment_for_stripe(payment, domain, scheme='https'):
    if not payment.stripe_product_id:
        product_id = create_product(name=str(payment.course.title) if payment.course else 'Оплата курса')
        payment.stripe_product_id = product_id

    if not payment.stripe_price_id:
        price_id = create_price(
            product_id=payment.stripe_product_id,
            amount_cents=int(payment.amount * 100),
            currency='rub'
        )
        payment.stripe_price_id = price_id

    success_url = f"{scheme}://{domain}/payments/stripe/success/?payment_id={payment.id}"
    cancel_url = f"{scheme}://{domain}/payments/stripe/cancel/?payment_id={payment.id}"
    session = create_checkout_session(payment.stripe_price_id, success_url, cancel_url)

    payment.stripe_session_id = session['id']
    payment.stripe_payment_url = session['url']
    payment.stripe_status = 'open'
    payment.save(update_fields=[
        'stripe_session_id', 'stripe_payment_url', 'stripe_status',
        'stripe_product_id', 'stripe_price_id'
    ])
    return payment