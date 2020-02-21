from django.db import models
from django.core.urlresolvers import reverse

from shop.models.model_utils import update_filename
from shop.utils import slugify
from shop.models import category, manufacturer


class Product(models.Model):
    category = models.ForeignKey(
        category.Category,
        related_name='products',
        verbose_name='Категорія')
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Назва')
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        null=True,
        blank=True,
        verbose_name='англ_назва')
    producer = models.ForeignKey(
        manufacturer.Manufacturer,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Виробник'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Ціна')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Створено')
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Оновлено')
    complex_product = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subitems',
        verbose_name='Компонентний товар')

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ('-created'
                    '',)
        index_together = (('id', 'slug'),)

    def is_complex(self):
        return len(self.subitems.all()) > 0

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.category.slug, self.id, self.slug])

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to=update_filename,
        null=True,
        blank=True,
        verbose_name='Фото')
    product = models.ForeignKey(
        Product,
        related_name='images',
        verbose_name='Фото'
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def _get_number_of_image(self):
        try:
            images = list(ProductImage.objects.filter(product__name=self.product.name))
            return images.index(self)
        except ValueError:
            return 0

    def __str__(self):
        return '№ ' + str(self._get_number_of_image() + 1)


class Feature(models.Model):
    name = models.CharField(max_length=20, verbose_name='Назва характеристики')
    slug = models.SlugField(
        max_length=30,
        null=True,
        blank=True,
        editable=False,
        verbose_name='англ_назва')
    category = models.ForeignKey(category.Category, verbose_name='Категорія товарів')
    is_digit = models.BooleanField(default=False, verbose_name='Числова х-ка')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ('-is_digit', 'name')

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Feature, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):

    feature = models.ForeignKey(Feature, verbose_name='Назва', related_name='feature_values')
    value = models.CharField(max_length=200, verbose_name='Значення')
    unit = models.CharField(max_length=5, verbose_name='Од. виміру', null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар')

    def __str__(self):
        return ' '.join([str(self.feature.name), str(self.value)])

    class Meta:
        verbose_name = 'Характеристика товару'
        verbose_name_plural = 'Характеристики товару'
        unique_together = (('feature', 'product'),)
