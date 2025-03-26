import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from decimal import Decimal

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    discount_code = models.CharField(max_length=20, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total accounting for delivery costs and discounts
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        
        # Convert settings to Decimal
        free_delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
        delivery_percentage = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / 100
        
        if self.order_total < free_delivery_threshold:
            self.delivery_cost = self.order_total * delivery_percentage
        else:
            self.delivery_cost = Decimal(0)
        
        # Apply discount before calculating grand total
        self.grand_total = (self.order_total - self.discount_amount) + self.delivery_cost
        self.grand_total = self.grand_total.quantize(Decimal('0.00'))
        self.save()

    def save(self, *args, **kwargs):
        """
        Override save method to set order number and handle decimals
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        
        # Ensure all decimal fields are properly quantized
        self.delivery_cost = Decimal(self.delivery_cost).quantize(Decimal('0.00'))
        self.order_total = Decimal(self.order_total).quantize(Decimal('0.00'))
        self.discount_amount = Decimal(self.discount_amount).quantize(Decimal('0.00'))
        self.grand_total = Decimal(self.grand_total).quantize(Decimal('0.00'))
    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product_size = models.CharField(max_length=20, null=True, blank=True)
    product_color = models.CharField(max_length=20, null=True, blank=True)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'