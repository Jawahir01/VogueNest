from django.shortcuts import render, redirect, get_object_or_404, reverse
from . import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, F
from django.db.models.functions import Lower
from django.conf import settings
from .models import Product, Category, Review, ProductImage, Size, Color
from .forms import ProductForm

def all_products(request):
    """Display all products with sorting and search"""
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sort_param = request.GET['sort']
            if sort_param == 'reset':
                # Reset sorting to default (no ordering)
                sort = None
                direction = None
            else:
                # Split the sort parameter into field and direction
                parts = sort_param.split('_')
                sort_field = parts[0]
                direction = parts[1] if len(parts) > 1 else 'asc'

                # Map sort_field to the correct sort key
                sortkey = sort_field
                if sort_field == 'name':
                    sortkey = 'lower_name'
                    products = products.annotate(lower_name=Lower('name'))
                elif sort_field == 'category':
                    sortkey = 'category__name'

                # Apply direction
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

                # Order the products
                products = products.order_by(sortkey)

                # Update sort and direction variables
                sort = sort_field
                direction = direction

        # Existing category and search filtering
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}' if sort and direction else 'None_None'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'all_categories': Category.objects.all(),
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """Display product details with images and reviews"""
    product = get_object_or_404(Product, pk=product_id)
    product_images = product.images.all().order_by('order')
    reviews = product.reviews.all().order_by('-created_at')

    context = {
        'product': product,
        'product_images': product_images,
        'reviews': reviews,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """Add product with image handling and order management"""
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('products')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product added successfully!")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Failed to add product. Please check the form.")
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'sizes': Size.objects.prefetch_related('categories').all(),
        'colors': Color.objects.prefetch_related('categories').all()
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """Edit product with image management"""
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('products')
    
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, "Failed to update product. Please check the form.")
    else:
        form = ProductForm(instance=product)
    
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """Delete product and associated images"""
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('products')

    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('products')

    return render(request, 'products/delete_product.html', {'product': product})

@login_required
def add_review(request, product_id):
    """Submit and handle product reviews"""
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    if request.method == 'POST':
        
        rating = int(request.POST.get('rating', 0))
        title = request.POST.get('title', '').strip()
        review_text = request.POST.get('review_text', '')

        if not (1 <= rating <= 5):
            messages.error(request, "Invalid rating value!")
            return redirect('product_detail', product_id=product.id)

        Review.objects.create(
            product=product,
            user=user,
            rating=rating,
            title=title,
            review_text=review_text
        )
        
        messages.success(request, "Review submitted successfully")

    return redirect('product_detail', product_id=product.id)