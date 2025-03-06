from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    product_count = 0

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
                total += quantity * product.price
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
            total += item_data * product.price
            product_count += item_data

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context