from django import forms
from django.core.validators import URLValidator
from .models import Product, Size, Color, ProductImage, Category

class ProductForm(forms.ModelForm):
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    image1_url = forms.URLField(
        label="Image 1 URL",
        required=True,
        help_text='Main product image URL'
    )
    image1 = forms.ImageField(
        label="Image 1",
        required=True,
        help_text='Main product image (600x600px minimum, 2MB max)'
    )
    image2_url = forms.URLField(
        label="Image 2 URL",
        required=True,
        help_text='Secondary product image URL'
    )
    image2 = forms.ImageField(
        label="Image 2",
        required=True,
        help_text='Secondary product image'
    )
    image3_url = forms.URLField(
        label="Image 3 URL",
        required=True,
        help_text='Additional product image URL'
    )
    image3 = forms.ImageField(
        label="Image 3",
        required=True,
        help_text='Additional product image'
    )
    image4_url = forms.URLField(
        label="Image 4 URL",
        required=True,
        help_text='Additional product image URL'
    )
    image4 = forms.ImageField(
        label="Image 4",
        required=True,
        help_text='Additional product image'
    )

    class Meta:
        model = Product
        fields = [
            'category', 'sku', 'name', 'description',
            'price', 'rating', 'sizes', 'colors',
            'image1_url', 'image1', 'image2_url', 'image2',
            'image3_url', 'image3', 'image4_url', 'image4'
        ]
        exclude = ('slug',)
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'step': 0.1
            }),
            'sizes': forms.CheckboxSelectMultiple(),
            'colors': forms.CheckboxSelectMultiple(),
            'image1_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image2_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image3_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image4_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        # Make images optional when editing existing product
        if self.instance.pk:
            for i in range(1, 5):
                self.fields[f'image{i}_url'].required = False
                self.fields[f'image{i}'].required = False

    def clean(self):
        cleaned_data = super().clean()
        images = [
            (cleaned_data.get('image1_url'), cleaned_data.get('image1')),
            (cleaned_data.get('image2_url'), cleaned_data.get('image2')),
            (cleaned_data.get('image3_url'), cleaned_data.get('image3')),
            (cleaned_data.get('image4_url'), cleaned_data.get('image4'))
        ]

        # Validate URLs
        url_validator = URLValidator()
        for url, _ in images:
            if url:
                try:
                    url_validator(url)
                except forms.ValidationError:
                    raise forms.ValidationError(f"Enter a valid URL: {url}")

        # Check image requirements
        if not self.instance.pk:  # New product
            if not all(url and img for url, img in images):
                raise forms.ValidationError("All four images and their URLs are required for new products")
        else:  # Existing product
            if any(url or img for url, img in images) and not all(url and img for url, img in images):
                raise forms.ValidationError("Provide all four images and their URLs or none to keep existing ones")

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 10:
            raise forms.ValidationError('Price must be greater than £10')
        return price

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        
        # First check if rating exists
        if rating is None:
            raise forms.ValidationError('Rating is required')
            
        # Then check the numerical bounds
        if not (0 <= rating <= 5):
            raise forms.ValidationError('Rating must be between 0 and 5')
            
        return rating

    def save(self, commit=True):
        product = super().save(commit=commit)
        images = [
            (self.cleaned_data.get('image1_url'), self.cleaned_data.get('image1')),
            (self.cleaned_data.get('image2_url'), self.cleaned_data.get('image2')),
            (self.cleaned_data.get('image3_url'), self.cleaned_data.get('image3')),
            (self.cleaned_data.get('image4_url'), self.cleaned_data.get('image4'))
        ]

        if any(url and img for url, img in images):
            product.images.all().delete()
            
            # Create new ProductImage instances with unique order
            for index, (url, img) in enumerate(images):
                if url and img:
                    is_featured = (index == 0)
                    ProductImage.objects.create(
                        product=product,
                        image_url=url,
                        image=img,
                        is_featured=is_featured,
                        order=index + 1
                    )

        return product