from django import forms
# from django.core.exceptions import ValidationError
from django.forms import BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('views_counter', 'slug', 'owner')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        taboo_world = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for data in taboo_world:
            if data in cleaned_data.lower():
                raise forms.ValidationError('Данное название не допустимо')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        taboo_world = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for data in taboo_world:
            if data in cleaned_data.lower():
                raise forms.ValidationError('Данное описание не допустимо')
        return cleaned_data


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'description', 'category',)


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        # fields = ('numb', 'name', 'is_actual')
        # exclude = ('is_actual',)
        fields = "__all__"
