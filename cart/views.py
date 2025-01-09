from django.shortcuts import render, redirect, reverse, HttpResponse
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


def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    quantity = int(request.POST.get('quantity'))
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
    else:
        if quantity > 0:
            cart[item_id] = quantity
        else:
            cart.pop(item_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
        else:
            cart.pop(item_id)
        
        request.session['cart'] = cart
        return HttpResponse(status=200)
        
    except Exception as e:
        return HttpResponse(status=500)
