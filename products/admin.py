from django.contrib import admin
from .models import Category, Product, ProductImage, Size, Color, Review

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'parent',
    )

    ordering = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
    )

    ordering = ('sku',)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'image',
        'order',
    )

    ordering = ('product',)

class SizeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'order',
    )

    ordering = ('order',)

class ColorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'hex_code',
    )

    ordering = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Review, ReviewAdmin)
