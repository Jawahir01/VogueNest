from django.contrib import admin
from .models import DiscountCode

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount_percent', 'active', 'used_count')
    list_filter = ('active',)
    search_fields = ('code',)