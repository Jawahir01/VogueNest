from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    # Add email field from User model
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Initialize form with user email"""
        super().__init__(*args, **kwargs)
        # Pre-populate email from User model
        self.fields['email'].initial = self.instance.user.email

        placeholders = {
            'email': 'Email Address', 
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_country': 'Country',
            'default_postcode': 'Postal Code',
        }

        # Remove the non-existent 'default_email' reference
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country' and field != 'email':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
