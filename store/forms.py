from django import forms
from .models import Product

class AddProductForm(forms.ModelForm):
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 1,
            'cols': 15,
            'class': 'form-control mb-3',  # ✅ Textarea should also get form-control
            'placeholder': 'Enter description Summary...'
        }),
        required=True
    )
    long_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 15,
            'class': 'form-control mb-3',  # ✅ Textarea should also get form-control
            'placeholder': 'Enter complete product description...'
        }),
        required=True
    )

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'price',
            'old_price',
            'short_description',
            'long_description',
            'is_featured',
            'is_available',
            'is_each'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['CheckboxInput', 'BooleanField']:
                # ✅ Apply checkbox styling
                field.widget.attrs.update({
                    'class': 'form-check-input',
                })
            else:
                # ✅ Apply regular input styling
                field.widget.attrs.update({
                    'class': 'form-control mb-3',
                })
