import requests
from .models import SearchItem
from shop.models import Product
from django.db.models import Q

STRIP_SYMBOLS = ('+', ',', ';')


def store(request, q):
    """Store queries in database"""
    if not request.session.get('q'): # save distinct search query in session to
        request.session['q'] = []    # reduce number of database storing operations
    if len(q) > 2:
        if q not in request.session['q']:
            request.session['q'].append(q)
            term = SearchItem()
            term.q = q
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(',')[0]
            else:
                client_ip = request.META.get('REMOTE_ADDR')
            term.ip_address = client_ip
            clients = SearchItem.objects.values('ip_address').filter(ip_address__contains=client_ip)
            if len(clients) == 0:
                try:
                    # Get geo data about IP from 2IP.ua API
                    url = 'http://api.2ip.ua/geo.json?ip=' + client_ip
                    geo_response = requests.get(url).json()
                    term.IP_location = geo_response['country'] + ', ' + geo_response['city']
                except Exception:
                    pass
            else:
                location = SearchItem.objects.values('IP_location').filter(ip_address=client_ip)
                term.IP_location = location[0]['IP_location']
            term.save()


def products(search_text, search_params, sort):
    """Return results of searching"""
    sort_dict = {'namea': 'name', 'pricea': 'price', 'named': '-name', 'priced': '-price'}
    words = prepare_words(search_text)
    products = Product.objects.all()
    results = Product.objects.none()  # generate empty queryset to chain search results for several words
    for word in words:
        results = (results | (products.filter(eval(get_filter_condition(search_params, word)))))
    if sort in sort_dict:
        return results.distinct().order_by(sort_dict[sort])
    return results.distinct()


def get_filter_condition(params, word) -> str:
    conditions = []
    for param in params:
        conditions.append("Q({param}__icontains='{word}')".format(param=param, word=word))
    conditions = ' | '.join(conditions) if len(params) > 1 else next(iter(conditions))
    return conditions


def prepare_words(search_text):
    """Prepare word for searching engine, remove strip_symbols"""
    for common in STRIP_SYMBOLS:
        if common in search_text:
            search_text = search_text.replace(common, ' ')
    words = search_text.split()
    return words[0:4]
