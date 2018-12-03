# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from views import MapList, CreateMapMessage, UpLoadFilesView, DownLoadFileView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'getTaskpackageList', MapList, base_name="tasks_list")


urlpatterns = [
    # url(r'^getTaskpackageList/$', MapList.as_view({'get': 'list'})),
    url(r'^taskackageDivision/$', CreateMapMessage.as_view()),
    url(r'^uploadTaskpackage/$', UpLoadFilesView.as_view()),
    url(r'^downloadTaskpackage/$', DownLoadFileView.as_view()),
]


urlpatterns += router.urls


