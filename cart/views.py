from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_cart(request):
    """ A view that renders the cart contents page """
    context = {
        'profile': request.user,
        }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, item_id):
    """ Add product with size/color variants to cart """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size')
    color = request.POST.get('product_color')
    cart = request.session.get('cart', {})

    variant_key = f"{size}_{color}" if size and color else str(size) if size else str(color)

    try:
        # Handle products with variants
        if size or color:
            if item_id in cart:
                if variant_key in cart[item_id]['variants']:
                    cart[item_id]['variants'][variant_key] += quantity
                else:
                    cart[item_id]['variants'][variant_key] = quantity
            else:
                cart[item_id] = {'variants': {variant_key: quantity}}
            
            messages.success(request, 
                f'Added {product.name} '
                f'{"Size: " + size.upper() + " " if size else ""}'
                f'{"Color: " + color.title() if color else ""} to cart'
            )
        
        # Handle products without variants
        else:
            if item_id in cart:
                cart[item_id] += quantity
            else:
                cart[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')

        request.session['cart'] = cart
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'Error adding item: {e}')
        return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your cart')
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)