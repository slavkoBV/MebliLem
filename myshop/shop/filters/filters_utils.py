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


def get_clean_values_list(values_list):
    clean_list = []
    for value in values_list:
        if hasattr(value, 'isdigit') and not value.isdigit():
            delimiter = next(i for i in value if not i.isdigit())
            clean_list.extend(value.split(delimiter))
        else:
            clean_list.append(value)
    return clean_list


def get_values_ranges(values):
    """

    :param values: list of values
    :return: list of ranges, such as ['0 - 99', '100 - 199'] etc.
    """
    result = []
    values = set(int(value) for value in get_clean_values_list(values))
    if values:
        number_of_ranges = int(1 + 3.322 * math.log10(len(values)))
        min_value = min(values)
        initial_min_value = min_value
        max_value = max(values)
        step = round((max_value - min_value) / number_of_ranges)
        for i in range(number_of_ranges):
            if i == number_of_ranges - 1 or step <= initial_min_value:
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
