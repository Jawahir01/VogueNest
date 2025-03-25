from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product
from .models import DiscountCode

# Create your views here.

def view_cart(request):
    """ A view that renders the cart contents page """
    context = {
        'profile': request.user,
        'cart': request.session.get('cart'),
        'discount': request.session.get('discount'),
        'discount_amount': request.session.get('discount_amount'),
        'discount_percent': request.session.get('discount_percent'),
        'discount_code': request.session.get('discount_code'),
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

def apply_discount(request):
    if request.method == 'POST':
        code = request.POST.get('discount_code', '').strip().upper()
        redirect_url = request.POST.get('redirect_url', 'cart/')
        
        try:
            discount = DiscountCode.objects.get(code=code)
            if discount.is_valid():
                request.session['discount_code'] = code
                discount.used_count += 1
                discount.save()
                messages.success(request, "Discount code applied successfully!")
            else:
                messages.error(request, "This discount code is no longer valid")
        except DiscountCode.DoesNotExist:
            messages.error(request, "Invalid discount code")
            
        return redirect(redirect_url)

def remove_discount(request):
    if 'discount_code' in request.session:
        code = request.session.pop('discount_code')
        messages.success(request, f"Discount code {code} removed successfully!")
    else:
        messages.error(request, "No discount code to remove")
    return redirect('view_cart')


def adjust_cart(request, item_id):
    """Adjust the quantity of items in the cart"""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')
    color = request.POST.get('product_color')
    cart = request.session.get('cart', {})

    try:
        # Handle products with variants
        if size or color:
            variant_key = f"{size}_{color}" if size and color else str(size) if size else str(color)
            
            if cart.get(str(item_id)) and cart[str(item_id)].get('variants'):
                if variant_key in cart[str(item_id)]['variants']:
                    if quantity > 0:
                        cart[str(item_id)]['variants'][variant_key] = quantity
                        messages.success(request, 
                            f'Updated {product.name} '
                            f'{"Size: " + size.upper() + " " if size else ""}'
                            f'{"Color: " + color.title() if color else ""} quantity to {quantity}'
                        )
                    else:
                        # Remove variant if quantity is 0 or less
                        del cart[str(item_id)]['variants'][variant_key]
                        messages.success(request, 
                            f'Removed {product.name} '
                            f'{"Size: " + size.upper() + " " if size else ""}'
                            f'{"Color: " + color.title() if color else ""} from cart'
                        )
                        
                        # Remove entire product entry if no variants left
                        if not cart[str(item_id)]['variants']:
                            del cart[str(item_id)]
                else:
                    messages.error(request, 'Variant not found in cart')
            else:
                messages.error(request, 'Product not found in cart')

        # Handle products without variants
        else:
            if str(item_id) in cart:
                if quantity > 0:
                    cart[str(item_id)] = quantity
                    messages.success(request, f'Updated {product.name} quantity to {quantity}')
                else:
                    del cart[str(item_id)]
                    messages.success(request, f'Removed {product.name} from cart')

        request.session['cart'] = cart
        return redirect(reverse('view_cart'))

    except Exception as e:
        messages.error(request, f'Error adjusting cart: {e}')
        return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size')
        color = request.POST.get('product_color')
        cart = request.session.get('cart', {})

        variant_key = f"{size}_{color}" if size and color else str(size) if size else str(color)

        # Handle products with variants
        if size or color:
            if str(item_id) in cart and 'variants' in cart[str(item_id)]:
                if variant_key in cart[str(item_id)]['variants']:
                    del cart[str(item_id)]['variants'][variant_key]
                    messages.success(request, 
                        f'Removed {product.name} '
                        f'{"Size: " + size.upper() + " " if size else ""}'
                        f'{"Color: " + color.title() if color else ""} from cart'
                    )
                    
                    # Remove entire product entry if no variants left
                    if not cart[str(item_id)]['variants']:
                        del cart[str(item_id)]
        # Handle products without variants
        else:
            if str(item_id) in cart:
                del cart[str(item_id)]
                messages.success(request, f'Removed {product.name} from cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)