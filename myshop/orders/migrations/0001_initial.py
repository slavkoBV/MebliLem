# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('first_name', models.CharField(verbose_name="Ім'я", max_length=100)),
                ('last_name', models.CharField(verbose_name='Прізвище', max_length=100)),
                ('email', models.EmailField(verbose_name='Ел. пошта', max_length=254)),
                ('address', models.CharField(verbose_name='Адреса', max_length=300)),
                ('phone', models.CharField(null=True, verbose_name='Моб. телефон', max_length=13, blank=True)),
                ('created', models.DateTimeField(verbose_name='Додано', auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачено')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('price', models.DecimalField(max_digits=10, verbose_name='Ціна', decimal_places=2)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кількість')),
                ('order', models.ForeignKey(to='orders.Order', verbose_name='товари', related_name='items')),
                ('product', models.ForeignKey(to='shop.Product', verbose_name='замовлені товари', related_name='order_items')),
            ],
        ),
    ]
