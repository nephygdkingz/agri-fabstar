from django import forms

COUNTRY_CHOICES = [
    ('Nigeria', 'Nigeria'),
    ('Ghana', 'Ghana'),
    ('Kenya', 'Kenya'),
    ('South Africa', 'South Africa'),
]

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "John",
            "required": "required"
        })
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Doe",
            "required": "required"
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "john@example.com",
            "required": "required"
        })
    )
    phone = forms.CharField(
        label="Phone",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+234 812 345 6789",
            "required": "required"
        })
    )
    address = forms.CharField(
        label="Address",
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123 Farm Road, City",
            "required": "required"
        })
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Anambra",
            "required": "required"
        })
    )
    country = forms.ChoiceField(
        label="Country",
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "required": "required"
        })
    )
