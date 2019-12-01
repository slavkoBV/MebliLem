import urllib.parse
from django import template
from django.utils.encoding import force_str

register = template.Library()


@register.simple_tag(takes_context=True)
def remove_from_query(context, *args, **kwargs):
    query_params = []
    for key, value_list in context['request'].GET._iterlists():
        if key not in args:
            if key in kwargs.keys():
                for value in kwargs.values():
                    if value not in value_list:  # TODO: Test this statement!!!
                        query_params.append((key, value))
            else:
                for value in value_list:
                    query_params.append((key, value))
    query_string = context['request'].path
    if len(query_params):
        query_string = '?%s' % urllib.parse.urlencode([(key, force_str(value))
                                                       for (key, value) in query_params if value]).replace('&', '&amp;')
    return query_string
