from django.db import models

from shop.models.model_utils import update_filename


class Catalog(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Назва')
    file = models.FileField(
        upload_to=update_filename,
        blank=True,
        null=True,
        verbose_name='Файл')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Додано')
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Оновлено')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
