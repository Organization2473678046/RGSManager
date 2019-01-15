# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from django.db import DatabaseError

# 定义错误处理方法,加入处理数据库错误的逻辑，数据库占位的错误
def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            print('[%s]: %s' % (view, exc))
            response = Response({'detail': u'服务器内部存储错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response