# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-22 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskpackages', '0022_remove_regiontask_servicename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regiontask',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
