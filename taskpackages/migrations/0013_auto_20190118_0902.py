# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-18 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskpackages', '0012_auto_20190117_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='regiontask',
            name='mapindexsde',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u63a5\u56fe\u8868sde'),
        ),
        migrations.AddField(
            model_name='regiontask',
            name='rgssde',
            field=models.CharField(max_length=1000, null=True, verbose_name='rgssde'),
        ),
    ]
