from django.shortcuts import render
from shop.utils import paginate
from search import search

from shop.models.product import Product

dict_message = {('1',): 'товар',
                ('2', '3', '4'): 'товари',
                ('0', '5', '6', '7', '8', '9'): 'товарів'}

sort_dict = {'namea': 'name', 'pricea': 'price', 'named': '-name', 'priced': '-price'}


def products_search_results(request):
    products = Product.objects.all()
    q = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    sort_param = sort_dict.get(sort, None)
    search_params = ('name', 'category__name')
    matches = search.search_objects(q, products, search_params, sort_param)
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
