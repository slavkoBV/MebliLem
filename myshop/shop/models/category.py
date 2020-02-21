from django.db import models
from django.core.urlresolvers import reverse

from shop.models.model_utils import update_filename
from shop.utils import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Категорія')
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        null=True,
        blank=True,
        verbose_name='англ_назва')
    image = models.ImageField(
        upload_to=update_filename,
        null=True,
        verbose_name='Зображення'
    )

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категорія'
        verbose_name_plural = 'категорії'

    def get_absolute_url(self):
        return reverse('shop:product_list', args=[self.slug])

    def __str__(self):
        return self.name
