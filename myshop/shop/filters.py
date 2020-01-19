import math
from django.db.models import Q

from shop.constants import DIMENSIONS


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
        max_value = max(values)
        step = round((max_value - min_value) / number_of_ranges)
        if number_of_ranges == 1:
            result.append(str(min_value) + '-' + str(max_value + 1))
        else:
            for i in range(number_of_ranges):
                if i == number_of_ranges - 1:
                    result.append(str(min_value) + '-' + str(max_value))
                else:
                    result.append(str(min_value) + '-' + str(min_value + step - 1))
                    min_value += step
    return result


def get_value_and_counts(object_list, values_list, value_name):
    """

    :param object_list: queryset of objects that have price attribute
    :param values_list: list of values ranges ex. ['200-400', '400-600', ...]
    :param value_name: name of value for which ranges are determined
    :return: list of tuples(value_range, number of objects that have value in value_range)
    """
    filter_condition = None
    if values_list:
        if isinstance(values_list[0], str):
            if isinstance(value_name, str):
                filter_condition = 'Q({}__range=(map(int, value.split("-"))))'.format(value_name)
            else:
                filter_condition = 'Q({name}__feature__name="{feature}")' \
                                   '& Q({name}__value__range=(map(int, value.split("-"))))'\
                    .format(feature=value_name[0], name=value_name[1])
        else:
            filter_condition = 'Q({}__name=value)'.format(value_name)
    if object_list and filter_condition:
        return [(value, object_list.filter(eval(filter_condition)).count()) for value in values_list]
    else:
        return [(value, 0) for value in values_list]


def get_filters(data: dict):
    filter_parameters = data.keys()
    filters = []
    for param in filter_parameters:
        if data[param]:
            if '-' in data[param]:
                if param in ('width', 'depth', 'height'):
                    filters.append(eval('Q(productfeature__feature__name="{feature}") '
                                        '& Q(productfeature__value__range=(map(int, "{value}".split("-"))))'
                                        .format(feature=DIMENSIONS[param][0], value=data[param])))
                else:
                    filters.append(eval('Q({}__range=(map(int, "{}".split("-"))))'.format(param, data[param])))
            else:
                filters.append(eval('Q({}__name="{}")'.format(param, data[param])))
    return filters
