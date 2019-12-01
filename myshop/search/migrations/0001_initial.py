# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('q', models.CharField(max_length=50)),
                ('search_date', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('IP_location', models.CharField(null=True, max_length=50, blank=True)),
            ],
            options={
                'verbose_name': 'Пошуковий запит',
                'verbose_name_plural': 'Пошукові запити',
                'ordering': ('search_date',),
            },
        ),
    ]
