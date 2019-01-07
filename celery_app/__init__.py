#!C:/Python27/ArcGISx6410.2/python.exe
# -*- coding:utf-8 -*-
"""
#============================================
#
# Project: mycelery
# Name: The file name is __init__.py
# Purpose: 
# Auther: Administrator
# Tel: 17372796660
#
#============================================
#
"""

from celery import Celery

app = Celery('celery_taskclip')

# 通过Celery 实例来加载配置模块
app.config_from_object('celery_app.celeryconfig')

