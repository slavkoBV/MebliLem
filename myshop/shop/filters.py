import math
from django.db.models import Q

from shop.constants import DIMENSIONS


class Filter:
    def __init__(self, filter_params):
        """

        :param filter_params: {'name': some_name, 'value': some_value}
        """
        self._filter_params = filter_params
        self.expression = None

    def get_expression(self):
        pass

    def build_filter_condition(self):
        self.expression = self.get_expression()
        return eval(self.expression.format(name=self._filter_params['name'], value=self._filter_params['value']))


class DimensionFilter(Filter):

    def __init__(self, filter_params):
        filter_params['name'] = DIMENSIONS[filter_params['name']]
        super().__init__(filter_params)

    def get_expression(self):
        return 'Q(productfeature__feature__name="{name}") &' \
               ' Q(productfeature__value__range=(map(int, "{value}".split("-"))))'


class ManufacturerFilter(Filter):
    def get_expression(self):
        return 'Q({name}__name="{value}")'


class PriceFilter(Filter):
    def get_expression(self):
        return 'Q({name}__range=(map(int, "{value}".split("-"))))'


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
    if values_list:
        if object_list:
            return [(value, object_list.filter(filter_mapping[value_name](
                {'name': value_name, 'value': value}
            ).build_filter_condition())
                     .count()) for value in values_list]
        else:
            return [(value, 0) for value in values_list]


def get_filters(data: dict):
    filters = [filter_mapping[param]({'name': param, 'value': value}).build_filter_condition()
               for param, value in data.items() if data[param]]
    return filters
