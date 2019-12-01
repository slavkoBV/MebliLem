from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'phone']

        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Напр., м. Львів, вул. Личаківська, д.3, кв. 1'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Напр., 067-123-45-67'})
        }
