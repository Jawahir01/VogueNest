from django.contrib import admin
from .models import Product, Category, ProductImage, Review

# Inline admin for Product Images
class ProductImageAdminInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Allows adding additional images

# Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
    )
    ordering = ('sku',)
    inlines = [
        ProductImageAdminInline,  # Now it’s defined before use
    ]

# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

# Review admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'rating',
        'created_at',
    )

# Register models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
admin.site.register(Review, ReviewAdmin)
