from collections import namedtuple

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects, size, request, context, var_name='object_list'):
    paginator = Paginator(objects, size)
    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    ON_EACH_SIDE = 2
    ON_ENDS = 3
    DOT = '...'
    page_num = object_list.number
    if paginator.num_pages <= 5:
        page_range = range(1, paginator.num_pages + 1)
    else:
        page_range = []
        if page_num > (ON_EACH_SIDE + ON_ENDS + 1):
            page_range.extend(range(1, ON_ENDS + 1))
            page_range.append(DOT)
            page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
        else:
            page_range.extend(range(1, page_num + 1))
        if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS):
            page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
            page_range.append(DOT)
            page_range.extend(range(paginator.num_pages - ON_ENDS + 1, paginator.num_pages + 1))
        else:
            page_range.extend(range(page_num + 1, paginator.num_pages + 1))

    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator
    context['DOT'] = DOT
    context['page_range'] = page_range

    return context


def slugify(sequence):
    translit_table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia',
        'ь': '', '\'': ''
    }
    forbidden_symbols = ('!', '?', '+', '*', '/', '=', '%', '^', '&', '$', '@', '(', ')', '[', ']', '{', '}', ',', '.')

    def translit(w):
        result = []
        if 'зг' in w:
            w = w.replace('зг', 'zgh')
        for i in w:
            if i in translit_table.keys():
                result.append(translit_table[i])
            elif i not in forbidden_symbols:
                result.append(i)
        return ''.join(result)

    words = sequence.strip().split(' ')
    if '' in words:
        words.remove('')
    return '-'.join(translit(word.lower()) for word in words)


MessageWords = namedtuple('MessageWords', ['singular', 'plural', 'plural_genitive'])


def get_message(number_of_items: int, nouns: MessageWords) -> str:
    """

    :param number_of_items: int
    :param nouns: namedtuple of ukrainian noun forms(singular, plural, plural in genitive case)
    :return: str
    """
    dict_message = {('1',): nouns.singular,
                    ('2', '3', '4'): nouns.plural,
                    ('0', '5', '6', '7', '8', '9'): nouns.plural_genitive}
    message = ''
    if len(str(number_of_items)) == 2 and str(number_of_items).startswith('1'):
        message = nouns.plural
    else:
        for i in dict_message.keys():
            if str(number_of_items)[-1] in i:
                message = dict_message[i]
    return message
