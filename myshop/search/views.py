from django.shortcuts import render
from shop.utils import paginate
from search import search

dict_message = {('1',): 'товар',
                ('2', '3', '4'): 'товари',
                ('0', '5', '6', '7', '8', '9'): 'товарів'}


def results(request):
    q = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    search_params = ('name', 'category__name')
    matches = search.products(q, search_params, sort)
    matches_len = len(matches)
    message = ''
    if len(str(matches_len)) == 2 and str(matches_len).startswith('1'):
        message = 'товарів'
    else:
        for i in dict_message.keys():
            if str(matches_len)[-1] in i:
                message = dict_message[i]

    context = paginate(matches, 12, request, {'matches': matches}, var_name='matches')
    context['q'] = q
    context['sort'] = sort
    context['matches_len'] = matches_len
    context['message'] = message
    search.store(request, q)
    return render(request, 'shop/product_search.html', context)
