from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import DiscountCode

def cart_contents(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0')
    subtotal = Decimal('0')
    product_count = 0
    discount_amount = Decimal('0')

    for item_id, item_data in cart.items():
        if isinstance(item_data, dict):
            product = Product.objects.get(pk=item_id)
            for variant_key, quantity in item_data['variants'].items():
                size, color = None, None
                if '_' in variant_key:
                    size, color = variant_key.split('_', 1)
                else:
                    size = variant_key if product.sizes.exists() else None
                    color = variant_key if product.colors.exists() else None
                
                cart_items.append({
                    'item_id': item_id,
                    'variant_key': variant_key,
                    'product': product,
                    'quantity': quantity,
                    'size': size,
                    'color': color,
                })
                item_price = product.price * quantity
                total += item_price
                subtotal += item_price
                product_count += quantity
        else:
            product = Product.objects.get(pk=item_id)
            cart_items.append({
                'item_id': item_id,
                'product': product,
                'quantity': item_data,
                'size': None,
                'color': None,
            })
            item_price = product.price * item_data
            total += item_price
            subtotal += item_price
            product_count += item_data

    discount_code = request.session.get('discount_code')
    discount = None
    if discount_code:
        try:
            code_obj = DiscountCode.objects.get(code=discount_code)
            if code_obj.is_valid():
                discount_amount = (total * code_obj.discount_percent / 100).quantize(
                    Decimal('0.00'), rounding=ROUND_HALF_UP
                )
                discount = {
                    'code': code_obj.code,
                    'percent': float(code_obj.discount_percent),
                    'amount': discount_amount
                }
                total -= discount_amount
        except DiscountCode.DoesNotExist:
            pass

    # Delivery calculation (based on discounted total)
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = (total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)).quantize(Decimal('0.00'))
        free_delivery_delta = (settings.FREE_DELIVERY_THRESHOLD - total).quantize(Decimal('0.00'))
    else:
        delivery = Decimal('0')
        free_delivery_delta = Decimal('0')
    
    grand_total = (delivery + total).quantize(Decimal('0.00'))
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'subtotal': subtotal,
        'product_count': product_count,
        'discount': discount,
        'discount_amount': discount_amount,
        'discount_code': discount_code,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context