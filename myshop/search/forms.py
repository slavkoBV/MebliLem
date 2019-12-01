from .models import SearchItem
from django import forms


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchItem
        fields = ('q',)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_text = 'Назва товару або категорії'
        self.fields['q'].widget.attrs['id'] = 'search'
        self.fields['q'].widget.attrs['class'] = 'form-control'
        self.fields['q'].widget.attrs['placeholder'] = default_text

    include = ('q',)
