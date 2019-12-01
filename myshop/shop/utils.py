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
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'Y',
        'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
        'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia',
        'ь': '', '\'': ''
    }
    replace_combinations = {'Zh': 'Zgh', 'zh': 'zgh'}
    forbidden_symbols = ('!', '?', '+', '*', '/', '=', '%', '^', '&', '$', '@', '(', ')', '[', ']', '{', '}', ',', '.')

    def translit(w):
        result = ''
        for i in w:
            if i in translit_table.keys():
                result += translit_table[i]
            elif i in forbidden_symbols:
                result += ''
            else:
                result += i
        if ('Зг' in w) or ('зг' in w):
            for i in replace_combinations.keys():
                if i in result:
                    result = result.replace(i, replace_combinations[i])
        return result

    words = sequence.strip().split(' ')
    return '-'.join(translit(word) for word in words).lower()
