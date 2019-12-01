# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Назва', max_length=100, blank=True)),
                ('file', models.FileField(null=True, verbose_name='Файл', upload_to='catalogs/', blank=True)),
                ('created', models.DateTimeField(verbose_name='Додано', auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
            ],
            options={
                'verbose_name': 'Каталог',
                'verbose_name_plural': 'Каталоги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(db_index=True, verbose_name='Категорія', max_length=200)),
                ('slug', models.SlugField(verbose_name='англ_назва', null=True, max_length=200, blank=True)),
                ('image', models.ImageField(null=True, verbose_name='Зображення', upload_to='categories/')),
            ],
            options={
                'verbose_name': 'категорія',
                'verbose_name_plural': 'категорії',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Назва характеристики', max_length=20)),
                ('category', models.ForeignKey(verbose_name='Категорія товарів', to='shop.Category')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Назва', max_length=64)),
                ('slug', models.SlugField(verbose_name='Коротка назва', null=True, max_length=64, blank=True)),
                ('image', models.ImageField(null=True, verbose_name='Логотип', upload_to='manufacturers/', blank=True)),
            ],
            options={
                'verbose_name': 'Виробник',
                'verbose_name_plural': 'Виробники',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(db_index=True, verbose_name='Назва', max_length=200)),
                ('slug', models.SlugField(verbose_name='англ_назва', null=True, max_length=200, blank=True)),
                ('price', models.DecimalField(max_digits=10, verbose_name='Ціна', decimal_places=2)),
                ('created', models.DateTimeField(verbose_name='Створено', auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('category', models.ForeignKey(to='shop.Category', verbose_name='Категорія', related_name='products')),
                ('complex_product', models.ForeignKey(null=True, to='shop.Product', verbose_name='Комплексний товар', related_name='subitems', blank=True)),
                ('producer', models.ForeignKey(null=True, to='shop.Manufacturer', verbose_name='Виробник', related_name='products', blank=True)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('value', models.CharField(verbose_name='Значення', max_length=200)),
                ('unit', models.CharField(null=True, verbose_name='Од. виміру', max_length=5, blank=True)),
                ('feature', models.ForeignKey(verbose_name='Назва', to='shop.Feature')),
                ('product', models.ForeignKey(verbose_name='Товар', to='shop.Product')),
            ],
            options={
                'verbose_name': 'Характеристика товару',
                'verbose_name_plural': 'Характеристики товару',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('image', models.ImageField(null=True, verbose_name='Фото', upload_to='products/', blank=True)),
                ('product', models.ForeignKey(to='shop.Product', verbose_name='Фото', related_name='images')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото',
            },
        ),
        migrations.AlterUniqueTogether(
            name='productfeature',
            unique_together=set([('feature', 'product')]),
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set([('id', 'slug')]),
        ),
    ]
