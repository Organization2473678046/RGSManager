#!C:/Python27/ArcGIS10.2/python.exe
#-*- coding:utf-8 -*-
"""
#============================================
#
# Project: mycelery
# Name: The file name is celeryconfig
# Purpose: 
# Auther: Administrator
# Tel: 17372796660
#
#============================================
#
"""
import os

#BORKER_URL='amqp://admin:Lantucx2018@localhost:5672/admin-vhost'
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

CELERY_RESULT_BACKEND ='amqp://'

CELERY_TIMEZONE='Asiz/Shanghai'


CELERY_QUEUES={
    'clip_tasks':{
        'exchange':'clip_tasks',
        'exchange_type':'direct',
        'binding_key':'clip_tasks'
    },
    'other_tasks': {
        'exchange': 'other_tasks',
        'exchange_type': 'direct',
        'binding_key': 'other_tasks'
    }
}

CELERY_DEFAULT_QUEUE='clip_tasks'

CELERY_IMPORTS=(
    'celery_app.clipfromsde',
    'celery_app.createregiontask'
    # 'celery_app.regionchunk'
)

#防止死锁
CELERY_FORCE_EXECV=True

#允许重试
CELERY_ACKS_LATE=True

#设置并发worker数量
CELERY_CONCURRENCY=2

#每个worker最多执行100个任务被销毁
CELERY_MAX_TASKS_PER_CHILD=100



