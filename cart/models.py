from django.db import models
from django.utils import timezone

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    max_usage = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)

    def is_valid(self):
        now = timezone.now()
        return (self.active and 
                self.used_count < self.max_usage and 
                self.valid_from <= now <= self.valid_to)

    def __str__(self):
        return self.code