# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-22 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskpackages', '0023_auto_20190222_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regiontask',
            name='name',
            field=models.CharField(error_messages={'unique': '\u9879\u76ee\u533a\u57df\u5df2\u5b58\u5728'}, max_length=200, null=True, unique=True, verbose_name='\u4efb\u52a1\u533a\u57df'),
        ),
    ]