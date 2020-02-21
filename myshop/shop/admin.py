from django import forms
from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.admin import AdminSite
from django.forms import BaseInlineFormSet

from shop.models.category import Category
from shop.models.manufacturer import Manufacturer
from shop.models.product import Product, ProductFeature, ProductImage, Feature
from shop.models.catalog import Catalog


class ProductFeatureFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        kwargs['parent_object'] = self.instance
        return super()._construct_form(i, **kwargs)

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            parent_object=self.instance,
        )
        self.add_fields(form, None)
        return form


class ProductFeatureForm(forms.ModelForm):

    class Meta:
        model = ProductFeature
        fields = ['feature', 'value', 'unit']
        name = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.parent_object = kwargs.pop('parent_object', None)
        super().__init__(*args, **kwargs)
        category = None
        if self.parent_object.id:
            category = Product.objects.get(id=self.parent_object.id).category
        self.fields['feature'].queryset = Feature.objects.filter(category=category)


class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature
    extra = 0
    formset = ProductFeatureFormSet
    form = ProductFeatureForm


class FeatureInline(admin.StackedInline):
    model = Feature
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [FeatureInline]


admin.site.register(Category, CategoryAdmin)


class ChangeProductPrice(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    percent = forms.DecimalField(label='Відсоток зміни ціни')


def change_product_price(modeladmin, request, queryset):
    form = None
    if 'apply' in request.POST:
        form = ChangeProductPrice(request.POST)

        if form.is_valid():
            percent = form.cleaned_data['percent']

            count = 0
            for item in queryset:
                item.price += item.price * percent / 100
                item.save()
                count += 1

            modeladmin.message_user(request, 'Ціну змінено у %d товарів' % count)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeProductPrice(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'shop/change_price.html', {'items': queryset, 'form': form, 'title': 'Зміна ціни'})


change_product_price.short_description = 'Зміна ціни товару'


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductInline(admin.StackedInline):
    model = Product
    fk_name = 'complex_product'
    extra = 0
    fields = ['name', 'category', 'slug', 'price']
    raw_id_fields = ['complex_product']
    verbose_name = 'Компонентний товар'
    verbose_name_plural = 'Компонентні товари'


admin.site.register(Manufacturer)


class IsComplexProductFilter(admin.SimpleListFilter):
    title = 'Комплексний товар'
    parameter_name = 'is_complex'

    def lookups(self, request, model_admin):
        return (
            ('Так', 'Так'),
            ('Ні', 'Ні')
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Так':
            return queryset.filter(subitems__gt=0).distinct()
        elif value == 'Ні':
            return queryset.exclude(subitems__gt=0).distinct()
        return queryset


class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'category', 'price', 'updated']
    list_filter = ['category', 'producer', IsComplexProductFilter]
    list_editable = ['price']
    list_per_page = 20
    list_max_show_all = 1000
    list_select_related = ('complex_product',)
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'producer', 'slug')
        }),
        ('Ціна/наявність', {
            'fields': ('price',)
        }),
    )
    inlines = [ProductImageInline, ProductFeatureInline, ProductInline]
    date_hierarchy = 'created'
    actions = [change_product_price, ]


admin.site.register(Product, ProductAdmin)


class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated']
    list_filter = ['created', 'updated']


AdminSite.site_header = 'Меблі Лем'
AdminSite.site_title = 'Адміністрування'
AdminSite.index_title = 'Меблі Лем Адміністрування'

admin.site.register(Catalog, CatalogAdmin)
