from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from products.models import Product
from cart.contexts import cart_contents
from cart.models import DiscountCode

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            
            # Add discount info
            current_cart = cart_contents(request)
            order.discount_code = current_cart.get('discount_code')
            order.discount_amount = current_cart['discount_amount']
            
            order.save()

            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(pk=item_id)
                    
                    # Handle products with variants
                    if isinstance(item_data, dict) and 'variants' in item_data:
                        for variant_key, quantity in item_data['variants'].items():
                            # Parse size and color from variant key
                            size, color = None, None
                            if '_' in variant_key:
                                size, color = variant_key.split('_', 1)
                            else:
                                # Handle single attribute variants
                                size = variant_key if product.sizes.exists() else None
                                color = variant_key if product.colors.exists() else None
                            
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                                product_color=color,
                            )
                    
                    # Handle products without variants
                    else:
                        quantity = item_data
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )

                except Product.DoesNotExist:
                    messages.error(request, "One of the products wasn't found. Please contact us!")
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty")
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = int(total * 100)
        
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Prefill form for authenticated users
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Handle discount usage tracking
    if order.discount_code:
        try:
            discount = DiscountCode.objects.get(code=order.discount_code)
            discount.used_count += 1
            discount.save()
        except DiscountCode.DoesNotExist:
            pass

    # Attach profile and clean session
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            # Save address logic here
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_country': order.country,
                'default_postcode': order.postcode,
            }

    # Clear session data
    if 'cart' in request.session:
        del request.session['cart']
    if 'discount_code' in request.session:
        del request.session['discount_code']

    messages.success(request, f' Your Order {order_number} processed successfully!')
    return render(request, 'checkout/checkout_success.html', {'order': order})