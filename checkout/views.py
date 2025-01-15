from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QE7vqBOTgvORfXXct9Sp4ce1Zhs1cT2eEwv32Y1lHTfCi9TBJOu0SiJYNRLHlkI8IUtjI0ErGw6XJqsQW8hY4sh00evVUSxg6',
        'client_secret': 'test client secret',
    }
    
    return render(request, template, context)
