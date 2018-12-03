# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
import views

router = routers.SimpleRouter()
router.register(r'^createuser/$', views.CreateUserView, base_name='create_user')
router.register(r'login/$', obtain_jwt_token, base_name='longin')
router.register(r'^workers/$', views.WorkerList, base_name='create_user')


urlpatterns = [
    url(r'^usermessage/$', views.RoleView.as_view())
]

urlpatterns += router.urls
