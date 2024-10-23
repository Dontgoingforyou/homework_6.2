from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Version

class ProductForm(forms.ModelForm):

    FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'purchase_price', 'manufactured_at']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(word in name.lower() for word in self.FORBIDDEN_WORDS):
            raise forms.ValidationError("Название продукта содержит запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(word in description.lower() for word in self.FORBIDDEN_WORDS):
            raise forms.ValidationError("Описание продукта содержит запрещенные слова.")
        return description


class ProductModeratorForm(ProductForm):
    class Meta:
        model = Product
        fields = ['description', 'category']


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']
        widgets = {
            'version_number': forms.TextInput(attrs={'class': 'form-control'}),
            'version_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
