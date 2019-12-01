from django import template
from ..forms import SearchForm

register = template.Library()


@register.inclusion_tag('tags/search_box.html')
def search_box(request):
    q = request.GET.get('q', '')
    form = SearchForm({'q': q})
    return {'form': form}
