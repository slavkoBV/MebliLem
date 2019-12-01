import urllib.parse
from django import template
from django.utils.encoding import force_str

register = template.Library()


@register.simple_tag(takes_context=True)
def modify_query(context, *params_to_remove, **params_to_change):
    """Render a link with modified current query parameters"""
    query_params = []
    for key, value_list in context['request'].GET._iterlists():
        if key not in params_to_remove:
            if key in params_to_change:
                query_params.append((key, params_to_change[key]))
                params_to_change.pop(key)
            else:
                for value in value_list:
                    query_params.append((key, value))
    for key, value in params_to_change.items():
        query_params.append((key, value))
    query_string = context['request'].path
    if len(query_params):
        query_string += '?%s' % urllib.parse.urlencode([(key, force_str(value))
                                                        for (key, value) in query_params if value])
        return query_string
