import math

from django.db.models import Max, Min

from shop.filters.filters import ManufacturerFilter, PriceFilter, DimensionFilter


filter_mapping = {
    'producer': ManufacturerFilter,
    'price': PriceFilter,
    'height': DimensionFilter,
    'width': DimensionFilter,
    'depth': DimensionFilter
}


def get_values_ranges(min_value, max_value, total_count):
    """ Return list of ranges, such as ['0 - 99', '100 - 199'] etc.

    """
    result = []
    # values = set(int(value) for value in get_clean_values_list(values))
    if total_count:
        number_of_ranges = int(1 + 3.322 * math.log10(total_count))
        step = round((max_value - min_value) / number_of_ranges)
        for i in range(number_of_ranges):
            if i == number_of_ranges - 1 or step <= 1:
                result.append(f"{min_value}-{max_value}")
                break
            else:
                result.append(f"{min_value}-{min_value + step-1}")
                min_value += step
    return result


def get_value_and_counts(object_list, values_list, value_name):
    """

    :param object_list: queryset of objects that have price attribute
    :param values_list: list of values ranges ex. ['200-400', '400-600', ...]
    :param value_name: name of value for which ranges are determined
    :return: list of tuples(value_range, number of objects that have value in value_range)
    """
    if values_list:
        if object_list:
            return [(value, object_list.filter(filter_mapping[value_name](
                {'name': value_name, 'value': value}
            ).build_filter_condition()).count()) for value in values_list]
        else:
            return [(value, 0) for value in values_list]


def get_filters(data: dict):
    filters = [filter_mapping[param]({'name': param, 'value': value}).build_filter_condition()
               for param, value in data.items() if data[param]]
    return filters


def get_price_range(object_list):
    max_price = int(object_list.aggregate(Max('price'))['price__max'])
    min_price = int(object_list.aggregate(Min('price'))['price__min'])
    return min_price, max_price
