# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-11 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskpackages', '0024_auto_20190222_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpackageowner',
            name='endtime',
            field=models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='taskpackageowner',
            name='starttime',
            field=models.DateTimeField(null=True, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]
