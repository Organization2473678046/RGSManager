# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.authentication import SessionAuthentication

"""RGSManageV3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from users.views import UserListViewSet,UserViewSet
from taskpackages.views import TaskPackageViewSet, TaskPackageSonViewSet, TaskPackageOwnerViewSet, \
    EchartTaskpackageViewSet, EchartScheduleViewSet, ScheduleViewSet, RegionTaskView, RegionTaskChunkUploadView

router = DefaultRouter()
router.register(r'users', UserListViewSet, base_name='users')
router.register(r'user', UserViewSet, base_name='user')
router.register(r'taskpackages', TaskPackageViewSet, base_name='taskpackage')
router.register(r'taskpackagesons', TaskPackageSonViewSet, base_name='taskpackageson')
router.register(r'taskpackageowners', TaskPackageOwnerViewSet, base_name='taskpackageowner')
router.register(r'echarttaskpackages', EchartTaskpackageViewSet, base_name='echarttaskpackage')
router.register(r'echartschedules', EchartScheduleViewSet, base_name='echartschedules')
router.register(r'schedule', ScheduleViewSet, base_name='schedule')
router.register(r'regiontasks', RegionTaskView, base_name='regiontasks')
# router.register(r'regiontaskschunk', RegionTaskChunkUploadView, base_name='regiontaskschunk')


urlpatterns = [
    url(r'^v8/admin/', admin.site.urls),
    # url(r'^v8/xadmin/', xadmin.site.urls),
    url(r'^v8/login/$', obtain_jwt_token),
    url(r'^v8/', include(router.urls)),
    url(r'^v8/docs/', include_docs_urls(title=u"库管系统API")),
    url(r'^v8/media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^v8/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

