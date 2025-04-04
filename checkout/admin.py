from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)  # Only include actual model fields here
    fields = ('product', 'quantity', 'product_size', 'product_color', 'lineitem_total')

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    
    readonly_fields = (
        'order_number', 'date', 'delivery_cost', 
        'order_total', 'grand_total', 'original_cart',
        'stripe_pid', 'discount_code', 'discount_amount'
    )
    
    fields = (
        'order_number', 'date', 'user_profile', 'full_name', 'email',
        'phone_number', 'street_address1', 'street_address2',
        'town_or_city', 'country', 'postcode', 'delivery_cost',
        'order_total', 'discount_code', 'discount_amount', 'grand_total',
        'original_cart', 'stripe_pid'
    )
    
    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'discount_amount', 'discount_code',
        'delivery_cost', 'grand_total',
    )
    
    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)