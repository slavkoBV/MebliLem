from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name='Ім\'я')
    last_name = models.CharField(
        max_length=100,
        verbose_name='Прізвище')
    email = models.EmailField(
        verbose_name='Ел. пошта')
    address = models.CharField(
        max_length=300,
        verbose_name='Адреса')
    phone = models.CharField(
        max_length=13,
        verbose_name='Моб. телефон',
        blank=True,
        null=True)
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Додано')
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Оновлено')
    paid = models.BooleanField(
        default=False,
        verbose_name='Оплачено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return 'Замовлення {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name='товари')
    product = models.ForeignKey(Product, related_name='order_items', verbose_name='замовлені товари')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    def __str__(self):
        return 'Замовлення {}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
