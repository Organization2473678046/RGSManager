# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-11 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskpackages', '0025_auto_20190311_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpackageowner',
            name='overdue',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u8d85\u671f'),
        ),
    ]
