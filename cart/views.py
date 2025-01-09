from django.shortcuts import render, redirect
from products.models import Product

# Create your views here.
def view_cart(request):
    """ A view to return cart """
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    """Add a quantity of the specified product to the shopping cart."""
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size')  # None if not provided
    color = request.POST.get('product_color')  # None if not provided

    cart = request.session.get('cart', {})

    if size:  # Product with sizes only
        if item_id in cart:
            if size in cart[item_id]['items_by_size']:
                cart[item_id]['items_by_size'][size] += quantity
            else:
                cart[item_id]['items_by_size'][size] = quantity
        else:
            cart[item_id] = {'items_by_size': {size: quantity}}

    elif color:  # Product with colors only
        if item_id in cart:
            if color in cart[item_id]['items_by_color']:
                cart[item_id]['items_by_color'][color] += quantity
            else:
                cart[item_id]['items_by_color'][color] = quantity
        else:
            cart[item_id] = {'items_by_color': {color: quantity}}

    else:  # Product with no size or color
        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

    request.session['cart'] = cart
    print(request.session['cart'])  # Debugging purposes

    return redirect(redirect_url)
