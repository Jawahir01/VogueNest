from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        sizes = cleaned_data.get('sizes') or []
        colors = cleaned_data.get('colors') or []

        if not category:
            raise forms.ValidationError("Category is required.")
        
        category_id = category.id
        errors = {}

        SIZE_RULES = {
            1: ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
            4: ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
            2: ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
            5: ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
            3: ['38/5', '39/6', '40/6.5', '41/7', '42/8'],
            6: ['38/5', '39/6', '40/6.5', '41/7', '42/8']
        }

        COLOR_RULES = {
            1: ['white', 'black'],
            4: ['white', 'black'],
            7: ['white', 'brown']
        }

        if category_id in [1, 4]:
            if not sizes or any(size not in SIZE_RULES[category_id] for size in sizes):
                errors['sizes'] = f"Shirts require sizes from {SIZE_RULES[category_id]}"
            if not colors or any(color not in COLOR_RULES[category_id] for color in colors):
                errors['colors'] = f"Shirts require colors from {COLOR_RULES[category_id]}"

        elif category_id in [2, 5]:
            if not sizes or any(size not in SIZE_RULES[category_id] for size in sizes):
                errors['sizes'] = f"Jeans require sizes from {SIZE_RULES[category_id]}"
            if colors:
                errors['colors'] = "Jeans shouldn't have colors"

        elif category_id in [3, 6]:
            if not sizes or any(size not in SIZE_RULES[category_id] for size in sizes):
                errors['sizes'] = f"Shoes require sizes from {SIZE_RULES[category_id]}"
            if colors:
                errors['colors'] = "Shoes shouldn't have colors"

        elif category_id == 7:
            if not colors or any(color not in COLOR_RULES[category_id] for color in colors):
                errors['colors'] = f"Bags require colors from {COLOR_RULES[category_id]}"
            if sizes:
                errors['sizes'] = "Bags shouldn't have sizes"

        elif category_id in [8, 9]:
            if sizes:
                errors['sizes'] = "Watches/Sunglasses shouldn't have sizes"
            if colors:
                errors['colors'] = "Watches/Sunglasses shouldn't have colors"

        if errors:
            for field, message in errors.items():
                self.add_error(field, message)

        return cleaned_data