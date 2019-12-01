from django.contrib import admin
from .models import SearchItem


class SearchTermAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'ip_address', 'IP_location', 'search_date')
    list_filter = ('ip_address', 'q', 'IP_location')

admin.site.register(SearchItem, SearchTermAdmin)
