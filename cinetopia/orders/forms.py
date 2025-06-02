from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'city', 'country', 'phone', 'note']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'address': 'Адрес доставки',
            'city': 'Город',
            'country': 'Страна',
            'phone': 'Телефон',
            'note': 'Комментарий к заказу',
        }