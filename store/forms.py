from django import forms
from .models import Product, ProductMedia
from django.forms import inlineformset_factory

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


class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ['image', 'is_featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_featured'].widget.attrs.update({
            'class': 'form-control mb-3 form-check-input'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control mb-3'
        })

        # ✅ Make 'image' optional for existing items that already have an image
        if self.instance and self.instance.pk and self.instance.image:
            self.fields['image'].required = False

    def clean_image(self):
        """
        ✅ Preserve existing image if no new one is uploaded
        """
        image = self.cleaned_data.get('image')
        if not image and self.instance and self.instance.pk:
            # No new image uploaded — keep the old one
            return self.instance.image
        return image

 
MediaFormSet = inlineformset_factory(
    Product, ProductMedia, form=ProductMediaForm,
    extra=4, can_delete=True, can_delete_extra=False
)

EditMediaFormSet = inlineformset_factory(
    Product, ProductMedia, form=ProductMediaForm,
    extra=2, can_delete=True, can_delete_extra=False
)
