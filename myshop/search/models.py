from django.db import models


class SearchItem(models.Model):

    q = models.CharField(max_length=50)
    search_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    IP_location = models.CharField(max_length=50, null=True, blank=True, default='Unknown')

    class Meta:
        verbose_name = 'Пошуковий запит'
        verbose_name_plural = 'Пошукові запити'
        ordering = ('search_date',)

    def __str__(self):
        return self.q
