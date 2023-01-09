from django import forms
from django.forms import widgets

from webapp.models import Product, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'balance', 'price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address']
