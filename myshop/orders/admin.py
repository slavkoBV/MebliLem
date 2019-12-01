from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_detail(obj):
    return '<a href="{}">Перегляд</a>'.format(reverse('orders:admin_order_detail', args=[obj.id]))


order_detail.allow_tags = True

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'phone', 'paid', 'created', 'updated', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
