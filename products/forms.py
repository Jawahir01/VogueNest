from django import forms
from .models import Product, Size, Color, ProductImage
from .widgets import MultipleFileInput

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
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'accept': 'image/*',
            'class': 'custom-file-input',
            'aria-label': 'Upload product images'
        }),
        required=False,
        help_text='Upload exactly 4 product images (600x600px minimum, 2MB max each)'
    )

    class Meta:
        model = Product
        fields = [
            'name', 'price', 'category', 'description', 
            'rating', 'sizes', 'colors', 'images'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'step': 0.1
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Initialize M2M fields
            self.fields['sizes'].initial = self.instance.sizes.all()
            self.fields['colors'].initial = self.instance.colors.all()
            
            # Get existing images count for validation
            self.existing_images_count = self.instance.images.count()

    def clean_images(self):
        images = self.files.getlist('images')
        total_images = len(images)
        
        if self.instance.pk:
            # Calculate total images when editing
            remaining_slots = 4 - self.existing_images_count
            if total_images > remaining_slots:
                raise forms.ValidationError(
                    f"You can only add {remaining_slots} more images (4 total allowed)"
                )
        else:
            # For new products, require exactly 4 images
            if total_images != 4:
                raise forms.ValidationError("Exactly 4 images are required")

        for image in images:
            # Validate file size
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    f"Image {image.name} exceeds 2MB limit"
                )

            # Validate image dimensions using Pillow
            from PIL import Image
            try:
                with Image.open(image) as img:
                    if img.width < 600 or img.height < 600:
                        raise forms.ValidationError(
                            f"Image {image.name} is too small (600x600px minimum)"
                        )
            except:
                raise forms.ValidationError(
                    f"Invalid image format for {image.name}"
                )

        return images

    def clean(self):
        cleaned_data = super().clean()
        # Ensure total images equals 4 (existing + new)
        if self.instance.pk:
            total_images = self.existing_images_count + len(cleaned_data.get('images', []))
            if total_images != 4:
                raise forms.ValidationError(
                    f"Total images must be 4 (currently {self.existing_images_count} existing)"
                )
        return cleaned_data

    def save(self, commit=True):
        # Save product first
        product = super().save(commit=commit)
        
        # Handle image uploads
        if commit and 'images' in self.cleaned_data:
            # Delete existing images if we're uploading new ones
            if self.instance.pk and self.cleaned_data['images']:
                product.images.all().delete()
                
            # Create new ProductImage instances
            for image in self.cleaned_data['images']:
                ProductImage.objects.create(product=product, image=image)

        return product