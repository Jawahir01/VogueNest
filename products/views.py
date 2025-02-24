from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Review, ProductImage
from django.db.models.functions import Lower
from profiles.models import UserProfile
from .forms import ProductForm



def all_products(request):

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(request, "Please inter your search!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products' : products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'profile': request.user,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
   
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
        'profile': request.user,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        review_text = request.POST.get('review', '')

        # Create a new review
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            review_text=review_text
        )
        review = Review.objects.create(product=product, user=user, rating=rating, review_text=review_text)
    
        return redirect('product_detail', product_id=product.id)

    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_product(request):
    """ Add a product to the store only by superuser """
    if not request.user.is_superuser:
        messages.error(request, 'Error, Unauthorized User')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add your product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'profile': request.user,
    }
    
    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store only by superuser """
    if not request.user.is_superuser:
        messages.error(request, 'Error, Unauthorized User.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'profile': request.user,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store only by superuser """
    if not request.user.is_superuser:
        messages.error(request, 'Error, Unauthorized User.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))