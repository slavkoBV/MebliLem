from functools import reduce
from operator import or_

import requests

from django.db.models import Q

from .models import SearchItem
from myshop.logger import logger

STRIP_SYMBOLS = ('+', ',', ';')
IP_API_URL = 'http://api.2ip.ua/geo.json?ip'


def store(request, q):
    """Store queries in database"""
    if not request.session.get('q'): # save distinct search query in session to
        request.session['q'] = []    # reduce number of database storing operations
        request.session.modified = True
    if len(q) > 2:
        if q not in request.session['q']:
            request.session['q'].append(q)
            request.session.modified = True
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
                    url = ''.join((IP_API_URL, '=', client_ip))
                    geo_response = requests.get(url).json()
                    term.IP_location = geo_response['country'] + ', ' + geo_response['city']
                except Exception as er:
                    logger.info(er)
            else:
                location = SearchItem.objects.values('IP_location').filter(ip_address=client_ip)
                term.IP_location = location[0]['IP_location']
            term.save()


def search_objects(search_text, object_list, search_params, sort):
    """Return results of searching"""

    words = prepare_words(search_text)
    results = object_list.model.objects.none()
    for word in words:
        results = (results | (object_list.filter(reduce(or_, get_filter_condition(search_params, word)))))
    if sort:
        return results.distinct().order_by(sort)
    return results.distinct()


def get_filter_condition(params, word):
    conditions = []
    for param in params:
        conditions.append(eval("Q({param}__icontains='{word}')".format(param=param, word=word)))
    return conditions


def prepare_words(search_text):
    """Prepare word for searching engine, remove strip_symbols"""
    for common in STRIP_SYMBOLS:
        if common in search_text:
            search_text = search_text.replace(common, ' ')
    words = search_text.split()
    return words[0:4]
