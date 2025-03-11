from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    slug = models.SlugField(max_length=254, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, 
                              on_delete=models.SET_NULL, 
                              related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Size(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='sizes')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)
    hex_code = models.CharField(max_length=7)
    categories = models.ManyToManyField(Category, blank=True, related_name="colors")

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='products')
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)    

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        return self.price * (1 - self.discount / 100)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.sku}")
            unique_slug = base_slug
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='')
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['product', 'order']

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_featured:
            ProductImage.objects.filter(product=self.product).update(is_featured=False)
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200, blank=True, null=True)  # Made optional
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}/5 - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
