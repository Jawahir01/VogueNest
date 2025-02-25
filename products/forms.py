from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category

class ProductForm(forms.ModelForm):
    # Define size choices
    CLOTHING_SIZES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]
    
    SHOE_SIZES = [
        ('38/5', '38 EU / 5 US'),
        ('39/6', '39 EU / 6 US'),
        ('40/6.5', '40 EU / 6.5 US'),
        ('41/7', '41 EU / 7 US'),
        ('42/8', '42 EU / 8 US'),
    ]

    # Define color choices
    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('brown', 'Brown'),
    ]

    sizes = forms.MultipleChoiceField(
        choices=CLOTHING_SIZES + SHOE_SIZES,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'size-selector'}
        ),
        required=False
    )
    
    colors = forms.MultipleChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'color-selector'}
        ),
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'
        image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        
        # Update widget classes
        for field_name, field in self.fields.items():
            if field_name not in ['sizes', 'colors']:
                field.widget.attrs['class'] = 'form-control border-black rounded-1'
        
        # Add category-specific initial settings
        if self.instance and self.instance.category:
            self.set_category_dependent_fields(self.instance.category.id)

    def set_category_dependent_fields(self, category_id):
        """Configure fields based on category"""
        # Hide/show fields based on category rules
        if category_id in [3, 6]:  # Shoes
            self.fields['sizes'].choices = self.SHOE_SIZES
            self.fields['colors'].widget = forms.HiddenInput()
        elif category_id in [1, 4, 2, 5]:  # Clothing
            self.fields['sizes'].choices = self.CLOTHING_SIZES
            self.fields['colors'].choices = [c for c in self.COLOR_CHOICES if c[0] in ['white', 'black']]
        elif category_id == 7:  # Bags
            self.fields['sizes'].widget = forms.HiddenInput()
            self.fields['colors'].choices = [c for c in self.COLOR_CHOICES if c[0] in ['white', 'brown']]
        elif category_id in [8, 9]:  # Accessories
            self.fields['sizes'].widget = forms.HiddenInput()
            self.fields['colors'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        sizes = cleaned_data.get('sizes') or []
        colors = cleaned_data.get('colors') or []

        if not category:
            raise forms.ValidationError("Category is required.")
        
        category_id = category.id
        errors = {}

        # Size validation rules
        SIZE_RULES = {
            1: self.CLOTHING_SIZES,
            4: self.CLOTHING_SIZES,
            2: self.CLOTHING_SIZES,
            5: self.CLOTHING_SIZES,
            3: self.SHOE_SIZES,
            6: self.SHOE_SIZES
        }

        # Color validation rules
        COLOR_RULES = {
            1: ['white', 'black'],
            4: ['white', 'black'],
            7: ['white', 'brown']
        }

        # Size validation
        if category_id in SIZE_RULES:
            allowed_sizes = [size[0] for size in SIZE_RULES[category_id]]
            if not sizes:
                errors['sizes'] = "Size selection is required for this category"
            elif any(size not in allowed_sizes for size in sizes):
                errors['sizes'] = f"Invalid sizes selected. Allowed sizes: {', '.join(allowed_sizes)}"

        # Color validation
        if category_id in COLOR_RULES:
            allowed_colors = COLOR_RULES[category_id]
            if not colors:
                errors['colors'] = "Color selection is required for this category"
            elif any(color not in allowed_colors for color in colors):
                errors['colors'] = f"Invalid colors selected. Allowed colors: {', '.join(allowed_colors)}"
        elif category_id in [3, 6, 8, 9]:  # Categories where colors are not allowed
            if colors:
                errors['colors'] = "Colors are not allowed for this category"

        if errors:
            for field, message in errors.items():
                self.add_error(field, message)

        # Image validation
        images = self.files.getlist('image')
        if len(images) != 4:
            self.add_error('image', 'Exactly 4 images are required')

        return cleaned_data