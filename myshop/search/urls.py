from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.products_search_results, name='search_results'),
]
