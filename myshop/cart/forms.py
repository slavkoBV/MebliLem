from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='Кількість',
        initial=1,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(
            attrs={'class': 'item_quantity'}
        )
    )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
