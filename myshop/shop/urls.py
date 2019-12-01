from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^delivery/$', views.delivery, name='delivery'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^about-us/$', views.about_us, name='about_us'),

    url(r'^$', views.main_page, name='main_page'),
    url(r'^catalogs/$', views.catalog_list, name='catalog_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]
