from django.db import models

from shop.models.model_utils import update_filename
from shop.utils import slugify


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Назва'
    )
    slug = models.SlugField(
        max_length=64,
        db_index=True,
        null=True,
        blank=True,
        verbose_name='Коротка назва')
    image = models.ImageField(
        upload_to=update_filename,
        blank=True,
        null=True,
        verbose_name='Логотип'
    )

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Виробник'
        verbose_name_plural = 'Виробники'

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.id)
