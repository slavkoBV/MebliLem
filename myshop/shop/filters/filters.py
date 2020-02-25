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
        return 'Q(dimension__feature__name="{name}") &' \
               ' Q(dimension__value__range=(map(int, "{value}".split("-"))))'


class ManufacturerFilter(Filter):

    def get_expression(self):
        return 'Q({name}__name="{value}")'


class PriceFilter(Filter):

    def get_expression(self):
        return 'Q({name}__range=(map(int, "{value}".split("-"))))'
