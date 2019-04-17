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
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

app = Celery('celery_taskclip')

# 通过Celery 实例来加载配置模块
app.config_from_object('celery_app.celeryconfig')


app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'over_time_task': {
            'task': 'celery_app.over_time.over_time',
            # 'schedule':  timedelta(seconds=20),
            'schedule':  crontab(minute=17, hour=14),
            'args': ()
        }
    }
)

