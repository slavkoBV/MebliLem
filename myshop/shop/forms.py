from django import forms


class ChoiceFieldNoValidation(forms.ChoiceField):
    """ChoiceField without validation because choices is determined dynamically

    """

    def validate(self, value):
        pass


class ProductFilterForm(forms.Form):
    producer = ChoiceFieldNoValidation(
        required=False
    )
    price = ChoiceFieldNoValidation(
        required=False
    )
    height = ChoiceFieldNoValidation(
        required=False
    )
    depth = ChoiceFieldNoValidation(
        required=False
    )
    width = ChoiceFieldNoValidation(
        required=False
    )
