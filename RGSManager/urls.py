# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""RGSManager URL Configuration

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

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import routers
from taskpackages.views import MapList, CreateMapMessage, CreateTaskpackageVersion, MapVersionList
from users.views import RoleView, WorkerList, CreateUserView
from rest_framework_jwt.views import obtain_jwt_token
from RGSManager.settings import MEDIA_ROOT
from django.views.static import serve


router = routers.DefaultRouter()
router.register(r'workers', WorkerList, base_name=u"workers")
router.register(r'getTaskpackageList', MapList, base_name=u"maplists")
# router.register(r'taskpackageversion', CreateTaskpackageVersion, base_name='taskpackageversion')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'login/', obtain_jwt_token),
    url(r'docs/', include_docs_urls(title=u"库管系统API", authentication_classes=[JSONWebTokenAuthentication, SessionAuthentication])),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^usermessage/$', RoleView.as_view()),
    url(r'^createuser/$', CreateUserView.as_view()),
    url(r'^taskackageDivision/$', CreateMapMessage.as_view()),
    url(r'^taskpackageversion/$', CreateTaskpackageVersion.as_view()),
    # url(r'^taskpackageversionlist/$', MapVersionList.as_view()),
]



