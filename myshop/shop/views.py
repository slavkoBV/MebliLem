from django.shortcuts import render, get_object_or_404
from django.db.models import Max, Min

from shop.models.category import Category
from shop.models.manufacturer import Manufacturer
from shop.models.product import Product, Dimension
from shop.models.catalog import Catalog

from cart.forms import CartAddProductForm
from shop.utils import paginate
from shop.filters.filters_utils import get_filters, get_value_and_counts, get_values_ranges, get_price_range
from shop.forms import ProductFilterForm
from shop.constants import DIMENSIONS


def main_page(request):
    categories = Category.objects.all()
    last_products = Product.objects.all().order_by('-created')[:8]
    manufacturers = Manufacturer.objects.all()
    return render(request, 'shop/main_page_1.html', {'categories': categories,
                                                     'last_products': last_products,
                                                     'manufacturers': manufacturers
                                                     })


def product_list(request, category_slug):

    sort_dict = {'namea': 'name', 'named': '-name', 'pasc': 'price', 'pdesc': '-price'}
    sort = request.GET.get('sort', '')
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    abs_min_price, abs_max_price = get_price_range(products)
    manufacturers = Manufacturer.objects.filter(products__in=products).distinct()

    dimensions = {
        DIMENSIONS[feature]: get_values_ranges([f['value'] for f in Dimension.objects.filter(
            feature__name=DIMENSIONS[feature], product__in=products).values()]) for feature in DIMENSIONS}

    data = {k: v for k, v in request.GET.items()}
    prices = data['price'].split('-') if data.get('price') else (None, None)
    max_price = prices[1] or abs_max_price
    min_price = prices[0] or abs_min_price
    form = ProductFilterForm(data=request.GET)

    if form.is_valid():
        data = form.cleaned_data
        filters = get_filters(data)
        if filters:
            for f in filters:
                products = products.filter(f)
    facets = {
        'selected': data,
        'categories': {
            'manufacturers': get_value_and_counts(products, manufacturers, value_name='producer'),
        },
    }
    # Update facets for dimensions
    facets['categories'].update(
        {dimension: get_value_and_counts(products, dimensions[DIMENSIONS[dimension]], value_name=dimension)
         for dimension in DIMENSIONS}
    )
    if any([data.get(k) for k in data.keys() if k != 'price']):
        abs_min_price, abs_max_price = get_price_range(products)
    if sort in sort_dict:
        products = products.order_by(sort_dict[sort])
    context = paginate(products, 20, request, {'products': products}, var_name='products')
    context['categories'] = categories
    context['category'] = category
    context['facets'] = facets
    context['min_price'] = min_price
    context['max_price'] = max_price
    context['abs_min_price'] = abs_min_price
    context['abs_max_price'] = abs_max_price

    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug, category_slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    subitems = product.subitems.all()
    product_features = product.productfeature_set.all().order_by('feature')
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'product_features': product_features,
                   'subitems': subitems,
                   'cart_product_form': cart_product_form})


def payment(request):
    return render(request, 'shop/payment.html', {})


def delivery(request):
    return render(request, 'shop/delivery.html', {})


def contacts(request):
    return render(request, 'shop/contacts.html', {})


def about_us(request):
    return render(request, 'shop/about_us.html', {})


def catalog_list(request):
    catalogs = Catalog.objects.all()
    return render(request, 'shop/catalogs.html', {'catalogs': catalogs})
