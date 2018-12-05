# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-03 10:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taskpackages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='\u4efb\u52a1\u5305\u540d\u79f0')),
                ('mapnums', models.CharField(blank=True, max_length=65536, null=True, verbose_name='\u56fe\u53f7')),
                ('file', models.FileField(blank=True, null=True, upload_to=taskpackages.models.user_directory_path, verbose_name='\u4efb\u52a1\u5305\u8def\u5f84')),
                ('status', models.CharField(default='0', max_length=16, verbose_name='\u4efb\u52a1\u5305\u72b6\u6001')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u903b\u8f91\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('describe', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u6587\u4ef6\u63cf\u8ff0')),
            ],
            options={
                'db_table': 'tb_taskpackage',
                'verbose_name': '\u4efb\u52a1\u5305\u540d\u79f0',
                'verbose_name_plural': '\u4efb\u52a1\u5305\u540d\u79f0',
            },
        ),
        migrations.CreateModel(
            name='TaskPackageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='v1.0', max_length=16, verbose_name='\u7248\u672c\u53f7')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u903b\u8f91\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('describe', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u6587\u4ef6\u63cf\u8ff0')),
                ('file', models.FileField(upload_to=taskpackages.models.user_directory_path, verbose_name='\u4efb\u52a1\u5305\u8def\u5f84')),
                ('taskpackage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taskpackageversion', to='taskpackages.TaskPackage', verbose_name='\u4efb\u52a1\u5305\u540d\u79f0')),
            ],
            options={
                'db_table': 'tb_taskpackageversion',
                'verbose_name': '\u4efb\u52a1\u5305\u7248\u672c',
                'verbose_name_plural': '\u4efb\u52a1\u5305\u7248\u672c',
            },
        ),
    ]
